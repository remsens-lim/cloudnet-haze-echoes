import xarray as xr
import numpy.ma as ma
import probability as prob
import numpy as np
import pandas as pd
import datetime
class ProbabilityCalculator:
    def __init__(self, classification_file, categorization_file ,path_to_save,
                 save_data = None,
                 ze_params=None,
                 vel_params=None,
                 beta_params=None,
                 threshold = None):
        self.classification_file = classification_file
        self.categorization_file = categorization_file
        self.load_dataset()
        self.ze_params   = ze_params or (-48, 6, True)  # Default values if not provided
        self.vel_params  = vel_params or (-2, 0.5, False)  # Default values if not provided
        self.beta_params = beta_params or (7, 0.8e-5, 5.0e-06, True)  # Default values if not provided
        self.threshold = threshold or 0.6
        self.save_data = save_data or False
        self.path_to_save = path_to_save
        self.calculate_probabilities()
        self.replace_with_new_value_conditional()




    def load_dataset(self):
        target_classification = xr.open_dataset(self.classification_file)
        target_categorization = xr.open_dataset(self.categorization_file)
        self.Ze  = target_categorization.Z.data
        self.vel = target_categorization.v.data
        self.betas = ma.masked_invalid(target_categorization.beta.data)*4
        self.height = target_categorization.height.data
        self.time = target_categorization.time.data
        self.classification = target_classification.target_classification.data
        self.cloud_base = target_classification.cloud_base_height_agl.data


    def get_probabilities(self, Ze, vel, betas, ze_params=None, vel_params=None, beta_params=None):
        if ze_params is None:
            ze_params = (-45, 5, True)  # Default values for loc, scale, and invert
        if vel_params is None:
            vel_params = (-1, 0.2, False)  # Default values for loc, scale, and invert
        if beta_params is None:
            beta_params = (6, 0.77e-5, 4.5e-06, False)  # Default values for shape, loc, scale, and invert

        loc_ze, scale_ze, invert_ze = ze_params
        loc_vel, scale_vel, invert_vel = vel_params
        loc_beta, scale_beta, shape_beta, invert_beta = beta_params

        Ze_prob  = prob.array_to_probability_radar(Ze, loc_ze, scale_ze, invert_ze)
        vel_prob  = prob.array_to_probability_radar(ma.masked_invalid(vel).filled(np.nan), loc_vel, scale_vel, invert_vel)
        beta_prob = prob.array_to_probability_ceilometer(betas, loc_beta, scale_beta, shape_beta, invert_beta)

        combined_prob = vel_prob.T * Ze_prob.T * beta_prob.T
        return Ze_prob, vel_prob, beta_prob, combined_prob


    def calculate_probabilities(self):
        self.Ze_prob, self.vel_prob, self.beta_prob, self.combined_prob = self.get_probabilities(self.Ze, self.vel,
                                                                                                 self.betas,
                                                                                                 self.ze_params,
                                                                                                 self.vel_params,
                                                                                                 self.beta_params)

    def replace_with_new_value_conditional(self):
        self.new_classification = prob.replace_with_new_value_conditional(self.classification,
                                                                          self.combined_prob,
                                                                          self.height,
                                                                          11,
                                                                          self.cloud_base,
                                                                          self.threshold)

    def save_dataset(self):
        dataset = xr.open_dataset(self.classification_file)
        # Create a new variable
        new_var = xr.DataArray(self.new_classification.T , coords=dataset.coords)
        dataset['target_classification_haze_echos'] = new_var

        # Add attributes to the specified variable
        dataset['target_classification_haze_echos'].attrs["units"] = ""
        dataset['target_classification_haze_echos'].attrs["long_name"] = "Target classification with haze echos"
        dataset['target_classification_haze_echos'].attrs["comment"] = ("This variable provides the main atmospheric target classifications\n"
                                                                        " with the haze echo classification that can be distinguished by radar and lidar\n"
                                                                        " (radar reflectivity, Doppler velocity and attenuted backscatter coefficient).\n"
                                                                        f"Parameters of the probability distribution:\n"
            f"radar reflectivity factor:   loc = {self.ze_params[0]},   scale = {self.ze_params[1]},  invert = {self.ze_params[2]}\n"
            f"Doppler velocity:  loc = {self.vel_params[0]},  scale = {self.vel_params[1]}, invert = {self.vel_params[2]}\n"
            f"Attenuated backscatter coefficient: loc = {self.beta_params[1]}, scale = {self.beta_params[2]}, shape = {self.beta_params[0]}, invert = {self.beta_params[3]}\n"
        )
        dataset['target_classification_haze_echos'].attrs["definition"] = (
            "\nValue 0: Clear sky.\n"
            "Value 1: Cloud liquid droplets only.\n"
            "Value 2: Drizzle or rain.\n"
            "Value 3: Drizzle or rain coexisting with cloud liquid droplets.\n"
            "Value 4: Ice particles.\n"
            "Value 5: Ice coexisting with supercooled liquid droplets.\n"
            "Value 6: Melting ice particles.\n"
            "Value 7: Melting ice particles coexisting with cloud liquid droplets.\n"
            "Value 8: Aerosol particles, no cloud or precipitation.\n"
            "Value 9: Insects, no cloud or precipitation.\n"
            "Value 10: Aerosol coexisting with insects, no cloud or precipitation."
            "Value 11: Haze echos."
        )
        dataset['target_classification_haze_echos'].attrs["_FillValue"] = -2147483647
        dataset['target_classification_haze_echos'].attrs["_ChunkSizes"] = [1440, 415]
        #print(dataset.time.data)
        date = pd.to_datetime(dataset.time.data[0])

        start_date = datetime.date(date.year, date.month,date.day)
        ymd = 10000*start_date.year + 100*start_date.month + start_date.day

        # Save the modified dataset with attributes
        dataset.to_netcdf(self.path_to_save + f'{ymd}_barbados_classification_new.nc')  # You can choose to overwrite the existing file or save to a new one
        print("Dataset saved to:", self.path_to_save)

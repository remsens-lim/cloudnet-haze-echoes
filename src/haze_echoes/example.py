from main import  ProbabilityCalculator
import plot_cloudnet as plot_cloudnet
import datetime
# Paths to Cloudnet products
path_to_classification_file    =  'CLASSIFICATION PATH'
path_to_categorization_file    =  'CATEGORIZATION PATH'

# adjust probability parameters if needed
# Default values for loc, scale, and invert
# ze_params = (-30, 5, True)
# vel_params = (-1, 0.2, False)

# Default values for shape, loc, scale, and invert
# beta_params = (6, 0.77e-5, 4.5e-06, False)
# probability_calculator = ProbabilityCalculator(path_to_classification_file, path_to_categorization_file, path_to_save, ze_params, vel_params, beta_params)

path_new_classification = 'NEW CLASSIFICATION PATH'
probability_calculator  = ProbabilityCalculator(path_to_classification_file,
                                                path_to_categorization_file,
                                                path_to_save=path_new_classification)
# Save the dataset as a new file
probability_calculator.save_dataset()

##############################################################################################
#                              PLOT PROBABILITY OVERVIEW
##############################################################################################

start_date = datetime.datetime(2021, 12,2,6,0,0 )
end_date   = datetime.datetime(2021, 12,2,8,0,0 )

# Plot overview new Cloudnet classification and variables with probabilities
fig = plot_cloudnet.plot_overview(start_date, end_date, probability_calculator)
plot_path = 'PLOT PATH'
fig.savefig(plot_path + f'probability_overview.png', dpi = 300)

# Creating dict to hold data with and without trend data for streamlined testing

training_sets = {'train': [target_train, features_train, target_val, features_val],
                'train_with_trend' : [target_with_trends_train, features_with_trends_train,
                                      target_with_trends_val, features_with_trends_val]}

# Building function to gridsearch multiple datasets and return relevent results

def test_classifiers(data, grid):
    results_dict = {}

    for data_set, splits in data.items():
        grid.fit(splits[1], splits[0])
        results_dict[data_set + ' results'] = [grid.best_score_, grid.best_params_, grid.score(splits[1], splits[0]), grid.score(splits[3], splits[2])]

    return results_dict

# Creating and Running GridSearch on Random Forest Model

from sklearn.ensemble import RandomForestClassifier

rft_param_grid = {'randomforestclassifier__n_estimators': [250, 350, 450],
                'randomforestclassifier__max_depth': [2, 6, 10, 14, 18, 22]}

rft_pipe = make_pipeline(RandomForestClassifier())

rft_grid = GridSearchCV(rft_pipe, rft_param_grid, scoring = "accuracy")

rft_results = test_classifiers(training_sets, rft_grid)

rft_results

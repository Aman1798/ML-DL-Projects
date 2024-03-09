#1 Load required libraries

library(psych)
library(stats)
library(readxl)
library(tidyverse)
library(corrplot)
library(ggplot2)
library(caret)
library(lmtest)
library(dplyr)
library(MASS)
library(car)
library(leaps)

#2 Load the dataset

# ***Note-Please change golf file path to load the file***
golf_path_file <- "~/Desktop/Github-Aman/ML-DL-Projects/GolfPredictions/Golf.txt"
golf <- data <- read.table(golf_path_file, header = TRUE, sep = " ")
head(golf)

#3 Check for missing values

colSums(is.na(golf))

#4 Separating the variables

golf$avg_winning <- golf$TotalWinnings / golf$Tournaments
other_variables <- dplyr::select(golf, AveStrokes, Driving, GIR, Putting, Birdie, SandSaves, Scrambling, PPR)

#5 Standardisation(Trying both scale and log) 
#(finally, used golf$avg_winning <- log(golf$TotalWinnings / golf$Tournaments))

#5.1 Standardise-Using Scale
golf$AveStrokes <- scale(golf$AveStrokes)
golf$Driving <- scale(golf$Driving)
golf$GIR <- scale(golf$GIR)
golf$Putting <- scale(golf$Putting)
golf$Birdie <- scale(golf$Birdie)
golf$SandSaves <- scale(golf$SandSaves)
golf$Scrambling <- scale(golf$Scrambling)
golf$PPR <- scale(golf$PPR)

golf$avg_winning <- scale(golf$TotalWinnings / golf$Tournaments)
head(golf)

#5.2 Standardise-Using Log
golf$AveStrokes <- log(golf$AveStrokes)
golf$Driving <- log(golf$Driving)
golf$GIR <- log(golf$GIR)
golf$Putting <- log(golf$Putting)
golf$Birdie <- log(golf$Birdie)
golf$SandSaves <- log(golf$SandSaves)
golf$Scrambling <- log(golf$Scrambling)
golf$PPR <- log(golf$PPR)

golf$avg_winning <- log(golf$TotalWinnings / golf$Tournaments)
head(golf)

#6 Summary Statistics

describe(golf$AveStrokes)
describe(golf$Driving)
describe(golf$GIR)
describe(golf$Putting)
describe(golf$Birdie)
describe(golf$SandSaves)
describe(golf$Scrambling)
describe(golf$PPR)
describe(golf$avg_winning)

#7 Correlation

#7.1 Correlation matrix
combined_data <- bind_cols(Average_Winnings = golf$avg_winning, other_variables)
combined_data_df <- as.data.frame(combined_data)
correlation_matrix <- cor(combined_data)

print(correlation_matrix)

correlation_order <- order(-abs(correlation_matrix[, "Average_Winnings"]))
correlation_matrix_sorted <- correlation_matrix[correlation_order, correlation_order]
sorted_variable_names <- colnames(correlation_matrix_sorted)

print(correlation_matrix_sorted)

correlation_matrix_sorted_df <- as.data.frame(as.table(correlation_matrix_sorted))
colnames(correlation_matrix_sorted_df) <- c("Variable1", "Variable2", "Correlation")
average_winnings_correlations <- correlation_matrix_sorted_df %>%
  filter(Variable1 == "Average_Winnings" | Variable2 == "Average_Winnings")

print(correlation_matrix_sorted_df)

#7.2 Correlation plots
print(correlation_matrix_sorted)
corrplot(correlation_matrix_sorted, method = "color", type = "upper", na.color = "white")

ggplot(average_winnings_correlations, aes(x = Variable1, y = Variable2, fill = Correlation)) +
  geom_tile() +
  theme_minimal() +
  labs(title = "Correlation Heatmap - Average Winnings vs Other Variables")

#8 Scatter and Pair plot

#8.1 Scatter Plots- Average Winning vs other variables

for (variable in names(other_variables)) {
  plot <- ggplot(combined_data, aes(x = !!sym(variable), y = Average_Winnings)) +
    geom_point(color = "#1f78b4") +
    theme_minimal() +
    labs(title = paste("Scatter Plot - Average Winning vs", variable),
         x = variable,
         y = "Average Winnings")
  
  print(plot)
}

#8.1 Pair Plots

selected_variables <- c("avg_winning", "AveStrokes", "Driving", "GIR", "Putting", "Birdie", "SandSaves", "Scrambling", "PPR")
selected_data <- golf[, selected_variables]
pairs(selected_data, col = "aquamarine",
      main = "Pairs Plot of Average winning and Other Variables",
      labels = selected_variables)

#9 Spliting in training and test data

set.seed(123)
train_index <- sample(1:nrow(golf), 0.8 * nrow(golf))
train_data <- golf[train_index, ]
test_data <- golf[-train_index, ]

#10 Linear Regression Models 
#(Tried 3 Linear models-Finally used 10.2 and 10.3 to show result in report)

#10.1 training_model-Using All variables
training_model <- lm(log(avg_winning) ~ AveStrokes + Driving + GIR + Putting + Birdie + SandSaves + Scrambling + PPR, data = train_data)

par(mfrow =c(2,2))
plot(training_model)
summary(training_model)

vif_values <- car::vif(training_model)
print(paste("VIF Values:", vif_values))

X <- model.matrix(training_model)

subset_model <- regsubsets(log(avg_winning) ~ AveStrokes + Driving + GIR + Putting + Birdie + SandSaves + Scrambling + PPR, data = train_data)

cp_values <- summary(subset_model)$cp

min_cp_index <- which.min(cp_values)
min_cp <- cp_values[min_cp_index]
min_model_size <- min_cp_index

summary(subset_model)
cat("Minimum Cp:", min_cp, "\n")
cat("Corresponding Model Size:", min_model_size, "\n")

training_predictions <- predict(training_model, newdata = train_data)
training_mse <- mean((log(training_predictions) - log(train_data$avg_winning))^2)
training_rmse <- sqrt(training_mse)

test_predictions <- predict(training_model, newdata = test_data)
test_mse <- mean((log(test_predictions) - log(test_data$avg_winning))^2)
test_rmse <- sqrt(test_mse)

print(paste("Mean squared error on training data:", training_mse))
print(paste("Mean squared error on testing data:", test_mse))
print(paste("Root mean squared error on training data:", training_rmse))
print(paste("Root mean squared error on testing data:", test_rmse))

#10.2 training model-With feature selection(using stepwise selection)
stepwise_model <- step(lm(log(avg_winning) ~ AveStrokes + Driving + GIR + Putting + Birdie + SandSaves + Scrambling + PPR, data = train_data))

X <- model.matrix(stepwise_model)

subset_model <- regsubsets(log(avg_winning) ~ AveStrokes + Driving + GIR + Putting + Birdie + SandSaves + Scrambling + PPR, data = train_data)

cp_values <- summary(subset_model)$cp

min_cp_index <- which.min(cp_values)
min_cp <- cp_values[min_cp_index]
min_model_size <- min_cp_index

cat("Minimum Cp:", min_cp, "\n")
cat("Corresponding Model Size:", min_model_size, "\n")

final_model <- lm(stepwise_model$terms, data = train_data)
par(mfrow = c(2, 2))
plot(final_model)
summary(final_model)

training_predictions <- predict(final_model, newdata = train_data)
training_mse <- mean((log(training_predictions) - log(train_data$avg_winning))^2)
training_rmse <- sqrt(training_mse)

test_predictions <- predict(final_model, newdata = test_data)
test_mse <- mean((log(test_predictions) - log(test_data$avg_winning))^2)
test_rmse <- sqrt(test_mse)

print(paste("Mean squared error on training data:", training_mse))
print(paste("Mean squared error on testing data:", test_mse))
print(paste("Root mean squared error on training data:", training_rmse))
print(paste("Root mean squared error on testing data:", test_rmse))


#No Perfect Multicollinearity
vif_values <- car::vif(final_model)
print(paste("VIF Values:",vif_values))


#10.3 training model-With feature selection(using stepwise selection)-Removed Outlier
outliers <- boxplot.stats(final_model$residuals)$out
train_data <- train_data[!final_model$residuals %in% outliers, ]

sw_model <- step(lm(log(avg_winning) ~ AveStrokes + Driving + GIR + Putting + Birdie + SandSaves + Scrambling + PPR, data = train_data))

last_model <- lm(sw_model$terms, data = train_data)
par(mfrow = c(2, 2))
plot(last_model)
summary(last_model)

training_predictions <- predict(last_model, newdata = train_data)
training_mse <- mean((log(training_predictions) - log(train_data$avg_winning))^2)
training_rmse <- sqrt(training_mse)

test_predictions <- predict(last_model, newdata = test_data)
test_mse <- mean((log(test_predictions) - log(test_data$avg_winning))^2)
test_rmse <- sqrt(test_mse)

print(paste("Mean squared error on training data:", training_mse))
print(paste("Mean squared error on testing data:", test_mse))
print(paste("Root mean squared error on training data:", training_rmse))
print(paste("Root mean squared error on testing data:", test_rmse))


#No Perfect Multicollinearity
vif_values <- car::vif(last_model)
print(paste("VIF Values:",vif_values)) 
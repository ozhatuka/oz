rm(list = ls())
###
#Q1
Ratings=read.csv("C:/Users/ozhat/Desktop/R/HW1/data.csv")
Ratings=Ratings[,1:3]
#Q2
library(ggplot2)
library(tidyr)
library(reshape2)
mat_ratings= Ratings %>% dcast(userId ~ movieId)
mat_ratings <- mat_ratings[,-1] # only ratings
#Q3
library(recommenderlab)

#Q4
M=as.matrix(mat_ratings)
real_mat_ratings=as(M,"realRatingMatrix") #this object should be realRatingMatrix 
real_mat_ratings 

#Q5
object.size(as(real_mat_ratings, "matrix")) / object.size(real_mat_ratings)
#A-Compression ratio is 89.9 bytes
#B-Saving a matrix as a realRatingMatrix object 
#  compactly stores sparse matrices(in my case:mat_ratings)
#c- Yes, This ratio matches expectations because 76,729,495 cells out of 77,215,000 
#   cells in total of mat_ratings are NA's(99.37%!)




#Q6
real_mat_ratings_filterd=real_mat_ratings[rowCounts(real_mat_ratings) >150,colCounts(real_mat_ratings) >150]


real_mat_ratings_filterd #838x817

#Q7
##for all similarity and distance methods:
pr_DB$get_entry_names()

similarity_users <-similarity(real_mat_ratings_filterd, method =
                                "Euclidean", which = "users")

similarity_items <-similarity(real_mat_ratings_filterd, method =
                                "Pearson", which = "items")

##Nothing to add here, just an example.  
#Convert your similarity object to matrix:
similarity_users_mat=as.matrix(similarity_users)
similarity_items_mat=as.matrix(similarity_items)
#Plots heatmap of the simialrity:
image(similarity_users_mat[1:10,1:10], 
      main = "User Euclidean similarity")
image(similarity_items_mat[1:10,1:10], 
      main = "User Pearson similarity")

#Q8
###List of models: (for realRatingMatrix)
recommender_models <- recommenderRegistry$get_entries(dataType =
                                                        "realRatingMatrix")
#display the model applicable to the realRatingMatrix
recommender_models
names(recommender_models)



###IBCF and UBCF default parameters:
recommender_models$IBCF_realRatingMatrix$parameters#IBCF parameters
recommender_models$UBCF_realRatingMatrix$parameters#UBCF parameters


#Model 1 parameters:
#recommender_models$.....$parameters
recommender_models$LIBMF_realRatingMatrix$parameters #LIBMF_realRatingMatrix parameters

#model 2 parameters:
recommender_models$SVD_realRatingMatrix$parameters #SVD_realRatingMatrix parameters



############PART A##############
################################
#Q9
#Defining the training and test sets 
#random indices (in our case randomly sampling 75-25 division)
set.seed(23)
which_train <- sample(x = c(TRUE, FALSE), size = nrow(real_mat_ratings_filterd),
                      replace = TRUE, prob = c(0.75, 0.25))



#train-test divisio
reco_data_train <- real_mat_ratings_filterd[which_train, ]
reco_data_test <- real_mat_ratings_filterd[!which_train, ]

#Q10
reco_model<-Recommender(data = reco_data_train, method = "SVD")

reco_model 

##Exploring the recommender model##
model_details <- getModel(reco_model)
model_details$description


#Q11
n_recommended <-5
reco_predicted<-predict(object = reco_model, newdata = reco_data_test,
                        n = n_recommended)

#Q12  
reco_matrix <- sapply(reco_predicted@items, function(x){
  colnames(real_mat_ratings_filterd)[x]
})

set.seed(1212)
Random_3_users=sample(1:dim(reco_data_test)[1],3)
reco_matrix[, Random_3_users]



#Q13
#defined for you:
min(rowCounts(real_mat_ratings_filterd))
items_to_keep <- min(rowCounts(real_mat_ratings_filterd))/2

rating_threshold <- 3.5

n_FOLD<-5

##
Scheme <- evaluationScheme(data =real_mat_ratings_filterd ,
                           method ="cross-validation" ,
                           k =n_FOLD ,
                           given =items_to_keep ,
                           goodRating =rating_threshold )

#Q14
model_1_to_evaluate <-"POPULAR" 
model_parameters <- NULL 
eval_recommender_1 <- Recommender(data = getData(Scheme, "train"),
                                  method = model_1_to_evaluate,
                                  parameter = model_parameters) 


model_2_to_evaluate <-"RANDOM"
model_parameters <- NULL 

eval_recommender_2 <- Recommender(data = getData(Scheme, "train"),
                                  method = model_2_to_evaluate,
                                  parameter = model_parameters)  

#Q15

items_to_recommend <-10  

eval_prediction_1 <- predict(object = eval_recommender_1,
                             newdata = getData(Scheme, "known"),
                             n = items_to_recommend,
                             type = "ratings")

eval_prediction_2 <- predict(object = eval_recommender_2 ,
                             newdata = getData(Scheme, "known") ,
                             n = items_to_recommend ,
                             type = "ratings" )


#Q16
eval_accuracy_1_by_user <- calcPredictionAccuracy(x = eval_prediction_1,
                                                  data = getData(Scheme, "unknown"),
                                                  byUser = TRUE)
eval_accuracy_1_by_user


#######
eval_accuracy_1<-calcPredictionAccuracy(x=eval_prediction_1,
                                        data=getData(Scheme, "unknown"),
                                        byUser=F )

eval_accuracy_1

eval_accuracy_2<-calcPredictionAccuracy(x=eval_prediction_2,
                                        data=getData(Scheme, "unknown"),
                                        byUser=F )

eval_accuracy_2
#RMSE extraction:
RMSE_1=eval_accuracy_1[1]
RMSE_2=eval_accuracy_2[1]

#Print the minimum RMSE:
min(RMSE_1,RMSE_2)


#Q17
#Models_to_evaluate <- list(

models_to_evaluate <- list(Model_1 =list(name = "IBCF", param = list(method = "Manhattan")),
                           Model_2 =list(name = "IBCF", param = list(method = "cosine")) ,
                           Model_3 =list(name = "UBCF", param = list(method = "Euclidean")) ,   
                           Model_4 =list(name = "UBCF", param = list(method = "Simpson")) ,
                           Model_5 =list(name = "SVD", param = NULL) ,
                           Model_6 =list(name = "ALS", param = NULL) )

#Q18 
n_recommendations <- c(1,5,9,seq(10, 100, 11))

list_results <- evaluate(x = Scheme,
                         method = models_to_evaluate ,
                         n = n_recommendations)
class(list_results) 


#########
avg_matrices <- lapply(list_results, avg) 
avg_matrices
head(avg_matrices$Model_3[, 5:8])
#########
#########
windows();plot(list_results, annotate = 1,
               legend = "topleft");title("ROC curve")
dev.off()

#Q19
#Name of the best model: model_4 - name = UBCF, method = "Simpson"



#Q20_Bonus:
vector_nn <- c(5, 10, 100, 150, 200, 450, 600) 


models_to_evaluate <- lapply(vector_nn, function(nn){ 
list(name = "UBCF", param = list(method = "Simpson", nn = nn)) }) 
names(models_to_evaluate) <- paste0("UBCF_nn_", vector_nn)

list_results <- evaluate(x = Scheme,
                         method = models_to_evaluate ,
                         n = n_recommendations)
windows();plot(list_results, annotate = 1, legend = "topleft");title("ROC curve")

#The optimal value is obtained when nn=450

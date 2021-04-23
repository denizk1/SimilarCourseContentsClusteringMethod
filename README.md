# SimilarCourseContentsClusteringMethod
A program that visually shows students the similarities of the courses in the departments they want to study


We want you to visually show the similarities of the courses in the departments they want to study to the students coming from abroad. In the file containing the codes, there are four text files containing the English course content of all the courses to be taught for four years (course contents were taken from any university website). The program reads and processes any course content file prepared in a similar format. As soon as the program starts to work, the user asks for the name of the course content file about the section that he is curious about the course groups and reads and processes the file. Then, first of all, the program creates the required word usage matrix to be grouped with some clustering techniques (Hierarchical or K-Means) using the course contents of this section and stores it in a text file. Then, the user individually asks and learns which clustering technique (Hierarchical or K-Means) and distance scale (Pearson, Euclid, or Tanimoto) they want to use. Finally, according to the clustering technique chosen, either the hierarchical cluster structure or the codes and names of the courses within each of the K number of cluster elements are written on the screen.


## Step 1 
Go to the directory where the project is

## Step 2
After typing "python main.py" in the command line, run it

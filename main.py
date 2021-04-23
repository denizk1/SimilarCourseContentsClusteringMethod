import string
from clusters import *
import sys

class HandleSectionContent(object):      #Our class that will process the file
    def __init__(self,lines):
        self.lines=lines
    def file_cleaning(self):       #In this method, unnecessary punctuation marks inside our file are extracted.
        result=""
        for c in open(self.lines,encoding="utf8").read().lower():
            if c not in string.punctuation:
                result+=c
        return result
    def handle(self):        # This method creates a list with course titles, a word list with course titles, and a dictionary with key words in the course titles, value sets giving the number of words in the course content, so that we can get the parameters that will form our original matrix.
        list=[i.split("\n") for i in HandleSectionContent(self.lines).file_cleaning().strip().split("\n\n")] # We extracted the file in paragraph form and then in line form and made it a list. Thus, it will be easier to get the elements we want.
        dict={}
        for i in list:
            dict[i[0]]=" ".join(i[1:]).split() # Thanks to the list we created, the keywords of our vocabulary are the lesson titles, and the values are the word lists in the lesson.
        wordcounts={}        #external dictionary holding lesson titles
        classlist=[]         #List of course titles
        feedlist=[]          # List of keywords (all words) we store in the dict dictionary
        for key,value in dict.items():
            apcount={}       # The inner loop is a dictionary that changes in each loop, with the key word and the value as the number of words.
            for i in value:
                feedlist.append(i)
                if i not in apcount:
                    apcount.setdefault(i,1)
                else:
                    apcount[i]+=1
            wordcounts[key]=apcount # the key of the external dictionary will be lecture titles, ask for values keyword with one more dictionary, request values will be a dictionary with word numbers
            classlist.append(key)
        return matrix(wordcounts,classlist,feedlist).matrix()
class matrix(object):   #our matrix class
    def __init__(self,wordcounts,classlist,feedlist):
        self.wordcounts=wordcounts
        self.classlist=classlist
        self.feedlist=list(set(feedlist)) #extracts the same words as all words will be examined one by one
    def matrix(self):
        wordlist=[] # We have defined an empty list required for word extraction. will only get the list of the words we need during the cycle
        for key in self.feedlist: # unnecessary words are stripped through the loop
            counter=0
            for value in self.classlist:
                if key in self.wordcounts[value]:
                    counter+=1
            frac=counter/len(self.classlist)
            if frac>0.1 and frac<0.5:
                wordlist.append(key)
        out=open("blogdata.txt",'w')   #Transferring matrix to a file
        out.write("LESSONS")
        for word in wordlist:    #the matrix is being created.
            out.write('\t{}'.format(word)) #words are written with each space left
        out.write('\n')  #bir alt satıra geçiyor
        for blog,inner_blog in self.wordcounts.items(): #It writes the number of words by using the external dictionary we have created. If the word is not in the content of the course title, it writes 0
            blog = blog.encode("ascii","ignore").decode("ascii")
            out.write(blog)
            for word in wordlist:
                if word in inner_blog:
                    out.write('\t{}'.format(inner_blog[word]))
                else:
                    out.write('\t0')
            out.write('\n')
        return "blogdata.txt"


if __name__ == "__main__":
    print("*****You can type exit at any time to exit*****")
    while True:   #operations and clusters will be done throughout the cycle
        try:
            filename=str(input("Enter the file name to be processed: "))
            if filename=="exit":
                sys.exit()
            matrix_filename=HandleSectionContent(filename).handle() # In order to create the matrix, we first need to edit the file and create a nested dictionary as here.
            cluster=str(input("Select the cluster management you want to handle:(k-means, hierarchical).If you want to process both (k-means and hierarchical):")).lower()
            if  cluster=="hierarchical":
                blognames, words, data = readfile(matrix_filename)
                try:
                    mesafe=input("Enter the distance measurement (euclid, pearson, tanamoto): ")
                    if mesafe=="exit":
                        sys.exit()
                    clust=hcluster(data,distance=eval(mesafe))    # hierarchical clustering is done. Hierarchical clustering; It takes the 2 course titles that are closest to each other and makes them into a single cluster and then cluster them with the closest ones.
                    printclust(clust,labels=blognames) #its output is being printed on the screen
                    drawdendrogram(clust, labels=blognames, jpeg = 'ExampleHierarchicalOutput.jpg') #Display on the figure for clearer understanding
                except NameError:
                    print("There is no such distance. Please try again!")
            elif cluster=="k-means":
                blognames, words, data = readfile(matrix_filename)
                try:
                    mesafe=input("Enter the distance measurement (euclid, pearson, tanamoto):")
                    if mesafe=="exit":
                        sys.exit()
                    kclust=kcluster(data,distance=eval(mesafe),k=10)  # Random clusters as many as the variable k are put forward and a list of the lesson headings closest to a proposed set is taken.
                    finished=[[blognames[r] for r in kclust[i]] for i in range(len(kclust))]
                    for i in finished:
                        print(i)  #outputs all the clusters formed
                except NameError:
                    print("There is no such distance. Please try again!")
            elif cluster=="hierarchical ve k-means" or cluster=="k-means and hierarchical":
                blognames, words, data = readfile(matrix_filename)
                try:
                    mesafe=input("Enter the distance measurement (euclid, pearson, tanamoto):")
                    if mesafe=="exit":
                        sys.exit()
                    clust=hcluster(data,distance=eval(mesafe))
                    printclust(clust,labels=blognames)
                    drawdendrogram(clust, labels=blognames, jpeg = 'ExampleHierarchicalOutput.jpg')
                    kclust=kcluster(data,distance=eval(mesafe),k=10)
                    finished=[[blognames[r] for r in kclust[i]] for i in range(len(kclust))]
                    for i in finished:
                        print(i)
                except NameError:
                    print("There is no such distance. Please try again!")
            elif cluster=="exit":
                sys.exit()
            elif cluster!="hierarchical" or cluster!="k-means" or cluster!="hierarchical ve k-means" or cluster!="k-means ve hierarchical" or cluster!="exit":
                print("Please enter the clustering technique or techniques correctly (hierarchical and k-means) or (k-means and hierarchical) or (hierarchical and k-means")
        except IOError:
            print("There is no such file! Please enter the file name correctly")

    # k-means clustering management is randomly reviewing. Hierarchical clustering deals with the most similar. So hierarchical clustering is a concrete and correct approach to my impressions.
    # In the k-means clustering technique, euclid distance and tanamoto distance give too many empty clusters. Each cluster at Pearson distance is full. Person takes a more concrete approach. He will surely find values
    # The reason why tanamoto and euclid give such empty sets is that they find values very close to any set that occurs in k-means against a number value they extract. It is not a very accurate calculation technique because most of them gather in the same place and very close values are obtained.

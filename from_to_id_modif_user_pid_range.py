from urllib import parse, request
import bs4 as bs
import os.path

# checking if image folder already exists, create one if not
if os.path.lexists(".\Images"):
    print("Image folder found")
else:
    print("Creating image folder...")
    os.makedirs(".\Images")

# save dir
os.chdir(".\Images")

# getting user inputs
user_pid_range = ''
val_entry = False
while val_entry is False:
    user_pid_range = input("Page range (x  y): ")
    user_pid_range = user_pid_range.split(" ")

    try:  # test if range is negative and if inputs are ints
        if int(user_pid_range[0]) > int(user_pid_range[1]):
            print("The provided range is negative.")
        else:
            val_entry = True
            print("validity to true")
            break

    except ValueError:
        print("Can't process input")

# make list for the for loop to iterate through
user_pid_range = list(range(int(user_pid_range[0])-1, int(user_pid_range[1])))

print(user_pid_range)

user_limit = ''
while isinstance(user_limit, int) is False:
    user_limit = input("How many picture(s) per page (max 100): ")
    try:
        user_limit = int(user_limit)
    except ValueError:
        print("That's not a number")
        continue

user_tags = input("Enter the tags please: ") or "rating:safe"

def post_retreive():

    # find posts and download content
    for urls in soup.find_all('post'):
        posts_list.append(urls)  # on ajoute les posts a une liste pour les référencer
        print(posts_list.index(urls) + 1)  # display the index +1
        print("- " + urls.get("file_url") + "\n")  # affiche les urls des images
        post_url = request.urlretrieve("https:" + urls.get("file_url"), urls.get("id")
                                       + "." + urls.get("file_url").split(".")[-1])  # dl and naming with respective ids
    return post_url

posts_list = []

for pages in user_pid_range:
    # encoding user inputs
    url_encoding = parse.urlencode({"tags": user_tags,
                                    "limit": user_limit, "pid": pages}, safe="=")
    tagged_url = "https://gelbooru.com/index.php?page=dapi&s=post&q=index&" + url_encoding

    print(tagged_url)  # display the final form of the url

    results = request.urlopen(tagged_url).read()  # url opening
    soup = bs.BeautifulSoup(results, "xml")  # making it a BS object

    post_retreive()

    #  print(urls.get("file_url").split(".")[-1])  # extention du media tétélchargé
    if pages == user_pid_range[-1]:
        print("======= Page {} cleared, stopping...=======".format(pages + 1))
    else:
        print("======= Page {} cleared, moving on to page {} =======".format(pages + 1, pages + 2))

print("{} image(s) on été téléchargée(s)".format(len(posts_list)))

# ideas :
# get wallpaper with a special tag
#

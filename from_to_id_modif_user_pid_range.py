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

# Welcoming message
print('''Hello and welcome to my Gelbooru image scrapper. First you will be required to enter how many pages you 
want to go through. You can enter a range of page, for example I want page 5 to 7 I will type: "5 7".
If I just want to start from the first one to another, first to tenth for example, I will type: "10".
After that you will be asked how many images do you want per page, there is a hard limit of 100 per page.
For the tags you can enter as many as you want, you have to separate them by a space.
Enjoy !\n''')

# getting user inputs
user_pid_range = ''
val_entry = False
while val_entry is False:
    user_pid_range = input("Page range (x  y): ")
    user_pid_range = user_pid_range.split(" ")

    try:  # test if range is negative, if inputs are ints, if inputs are 1 or 2 numbers

        if len(user_pid_range) < 2:  # if the input is only one number
            user_pid_range[0] = int(user_pid_range[0])  # test if int
            val_entry = True
            print("validity to true")
            user_pid_range = list(range(0, int(user_pid_range[0])))  # generate a range of pages

        elif len(user_pid_range) > 2:
            print("You entered more than 2 numbers")

        else:
            if int(user_pid_range[0]) > int(user_pid_range[1]):  # are the input positive
                print("The provided range is negative.")

            else:
                val_entry = True
                print("validity to true")
                user_pid_range = list(range(int(user_pid_range[0])-1, int(user_pid_range[1])))  # generate rng of pages

    except ValueError:
        print("Can't process input")

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

post_url = ''
def post_retreive():

    global post_url

    for urls in soup.find_all('post'):
        posts_list.append(urls)  # on ajoute les posts a une liste pour les référencer
        print(posts_list.index(urls) + 1)  # display the index +1
        print("- " + urls.get("file_url") + "\n")  # affiche les urls des images
        try:
            post_url = request.urlretrieve("https:" + urls.get("file_url"), urls.get("id")
                                           + "." + urls.get("file_url").split(".")[-1]) # dl and naming with respective ids
        except request.HTTPError:
            print("The post couldn't be retrieved")

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

from urllib import parse, request
import bs4 as bs
import os.path
import time

# checking if image folder already exists, create one if not
if os.path.lexists(".\Images"):
    print("Image folder found\n")
else:
    print("Creating image folder...\n")
    os.makedirs(".\Images")

# save dir
os.chdir(".\Images")

# Welcoming message
print('''Hello and welcome to my Gelbooru image scrapper. \n''')

starting_page = ""
while isinstance(starting_page, int) is False:
    starting_page = input("At what page should it start: ")
    try:
        starting_page = int(starting_page)
        if starting_page <= 0:

            starting_page = 1
    except ValueError:
        print("Please enter a valid number")

starting_page -= 1

user_pictures = ""
while isinstance(user_pictures, int) is False:
    user_pictures = input("Number of picture: ")
    try:
        user_pictures = int(user_pictures)
    except ValueError:
        print("Please enter a valid number")

pages = 0
alone_picture = user_pictures

if user_pictures >= 100:
    user_pictures = str(user_pictures)
    user_pictures = user_pictures[:-2] + "." + user_pictures[-2:]
    user_pictures = str(user_pictures).split(".")
    pages, alone_picture = user_pictures

print("It will ask for:", end="")
if int(pages) > 0:
    print(" {} pages of 100 images,".format(pages), end="")

if int(alone_picture) > 0:
    print(" 1 pages of {} images,".format(alone_picture), end="")

print(" starting page {}.".format(starting_page + 1))

if int(alone_picture) > 0:
    page_range = list(range(starting_page, starting_page + int(pages) + 1))
else:
    page_range = list(range(starting_page, starting_page + int(pages)))

user_tags = input("Enter the tags please: ") or "rating:safe"
print(page_range)
posts_list = []

for page in page_range:
    # encoding user inputs
    if int(alone_picture) != 0 and page == page_range[-1]:
        url_encoding = parse.urlencode({"tags": user_tags, "limit": alone_picture, "pid": page}, safe="=")
        tagged_url = "https://gelbooru.com/index.php?page=dapi&s=post&q=index&" + url_encoding
    else:
        url_encoding = parse.urlencode({"tags": user_tags, "limit": 100, "pid": page}, safe="=")
        tagged_url = "https://gelbooru.com/index.php?page=dapi&s=post&q=index&" + url_encoding

    print(tagged_url)  # display the final form of the url

    results = request.urlopen(tagged_url).read()  # url opening
    soup = bs.BeautifulSoup(results, "xml")  # making it a BS object

    for urls in soup.find_all('post'):
        posts_list.append(urls)  # add post to a list to index them
        print(posts_list.index(urls) + 1)  # display the index +1
        print("- " + urls.get("file_url") + "\n")  # display the picture url

        try:  # dl and naming with respective ids

            request.urlretrieve("https:" + urls.get("file_url"), urls.get("id")
                                + "." + urls.get("file_url").split(".")[-1])

        except request.HTTPError:
            print("The post couldn't be retrieved")
            # time.sleep(3)  # no need for that yet / incomplete fucntion
            # print("Retrying...")

    #  print(urls.get("file_url").split(".")[-1])  # extention of the media
    if page == page_range[-1]:
        print("======= Page {} cleared, stopping...=======".format(page + 1))
    else:
        print("======= Page {} cleared, moving on to page {} =======".format(page + 1, page + 2))
        time.sleep(2)

print("{} image(s) have been downloaded".format(len(posts_list)))
input("Press Enter to quit")

# ideas :
# get wallpaper with a special tag
# make a % count
#

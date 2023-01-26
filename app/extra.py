# Function for finding the post with particular id
def find_post(id):
    for i in posts:
        if i['id']==id:
            return i

def find_post_index(id,i):
    for post in posts:
        i=i+1
        if post['id']==id:
            return (post,i)
    
    return (None,-1)
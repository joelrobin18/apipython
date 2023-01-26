# Function for finding the post with particular id
posts=[]
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

# try:
#     conn=db.connect(host="blaaaa",
#                             database="blaaaaa", 
#                             user="blaaaa",
#                             password="1234567890")
    
#     cursor=conn.cursor()
#     print("Database Successfully Connected")
# except Exception as error:
#     print("Error",error)
#     pass

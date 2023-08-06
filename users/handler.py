from random import randint

def handle_uploaded_file(f):
    name=str(f).split('.')[0]
    ext=str(f).split('.')[1]
    ran=str(randint(1000,100000))
    new_name=''
    new_name+=''.join([name,ran,'.',ext])

    with open(f'media/prescription/{new_name}','wb') as file :
        for chunk in f.chunks():
            file.write(chunk)
    return f'{new_name}'
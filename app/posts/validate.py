# posts/validate.py
# Written by Jeff Kaleshi

IMAGE_EXTENSIONS = [
    'png',
    'jpg',
    'jpeg',
    'gif',
]

DOCUMENT_EXTENSIONS = [
    'text',
    'pdf',
    'doc',
    'xls',
    'ppt',
]

def validate_new_post(post_data):
    '''
        Checks if the updated new post form is valid
        :post_data: {}}
        :return: String
    '''
    errors = []
    if post_data['body'] == None:
        errors.append('Missing Body!')
    if post_data['title'] == None:
        errors.append('Missing Title!')
    if post_data['post_type'] == None:
        errors.append('Missing Type!')

    if post_data['images'] != None:
        image_errors = validate_files(post_data['images'], 'images', IMAGE_EXTENSIONS)
        if image_errors != '':
            errors.append(image_errors)

    if post_data['documents'] != None:
        document_errors = validate_files(post_data['documents'], 'documents', DOCUMENT_EXTENSIONS)
        if document_errors != '':
            errors.append(document_errors)

    return errors

def validate_update_post(post_data):
    '''
        Checks if the updated post form is valid
        :post_data: {}}
        :return: String
    '''
    error = ''
    body_exists = post_data.get('body') != None
    title_exists = post_data.get('title') != None
    type_exists = post_data.get('post_type') != None
  
    if not body_exists and not title_exists and not type_exists:
        error = 'No parameters to update!'

    return error

def valid_file(filename, extensions):
    '''
        Checks if the file extension is valid
        :filename: String
        :extensions: [str, str, ...]
        :return: boolean
    '''
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in extensions


def validate_files(files, file_type, allowed_extensions):
    '''
        Checks if files are valid based on the 
        file extension type passed in
        :files: MultiDict
        :file_type: String
        :allowed_extensions: [str, str, ...]
        :return: String
    '''
    message = ''
    for file in files:
        if not valid_file(file.filename, allowed_extensions):
            files_valid = False
            message = 'One or more {} have an invalid extension!'.format(file_type)
            break
    
    return message
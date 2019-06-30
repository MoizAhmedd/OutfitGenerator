from google.cloud import vision
from google.cloud import vision
from google.oauth2 import service_account
import os

credentials = service_account.Credentials.from_service_account_file(r'C:\Users\ahmed\Documents\Summer2019\GCPCredentials\outfitgenerator-2e7110750cf6.json')
def create_product_set(
        project_id, location, product_set_id, product_set_display_name):
    """Create a product set.
    Args:
        project_id: Id of the project.
        location: A compute region name.
        product_set_id: Id of the product set.
        product_set_display_name: Display name of the product set.
    """
    client = vision.ProductSearchClient(credentials = credentials)

    # A resource that represents Google Cloud Platform location.
    location_path = client.location_path(
        project=project_id, location=location)

    # Create a product set with the product set specification in the region.
    product_set = vision.types.ProductSet(
            display_name=product_set_display_name)

    # The response is the product set with `name` populated.
    response = client.create_product_set(
        parent=location_path,
        product_set=product_set,
        product_set_id=product_set_id)

    # Display the product set information.
    print('Product set name: {}'.format(response.name))
    print('Product display name:{}'.format(response.display_name))

def create_product(
        project_id, location, product_id, product_display_name,
        product_category):
    """Create one product.
    Args:
        project_id: Id of the project.
        location: A compute region name.
        product_id: Id of the product.
        product_display_name: Display name of the product.
        product_category: Category of the product.
    """
    client = vision.ProductSearchClient(credentials=credentials)

    # A resource that represents Google Cloud Platform location.
    location_path = client.location_path(project=project_id, location=location)

    # Create a product with the product specification in the region.
    # Set product display name and product category.
    product = vision.types.Product(
        display_name=product_display_name,
        product_category=product_category)

    # The response is the product with the `name` field populated.
    response = client.create_product(
        parent=location_path,
        product=product,
        product_id=product_id)


    # Display the product information.
    print('Product name: {}'.format(response.display_name))

def add_product_to_product_set(
        project_id, location, product_id, product_set_id):
    """Add a product to a product set.
    Args:
        project_id: Id of the project.
        location: A compute region name.
        product_id: Id of the product.
        product_set_id: Id of the product set.
    """
    client = vision.ProductSearchClient(credentials=credentials)

    # Get the full path of the product set.
    product_set_path = client.product_set_path(
        project=project_id, location=location,
        product_set=product_set_id)

    # Get the full path of the product.
    product_path = client.product_path(
        project=project_id, location=location, product=product_id)

    # Add the product to the product set.
    client.add_product_to_product_set(
        name=product_set_path, product=product_path)
    print('Product added to product set.')


def update_product_labels(
        project_id, location, product_id, key, value):
    """Update the product labels.
    Args:
        project_id: Id of the project.
        location: A compute region name.
        product_id: Id of the product.
        key: The key of the label.
        value: The value of the label.
    """
    client = vision.ProductSearchClient(credentials=credentials)

    # Get the name of the product.
    product_path = client.product_path(
        project=project_id, location=location, product=product_id)

    # Set product name, product label and product display name.
    # Multiple labels are also supported.
    key_value = vision.types.Product.KeyValue(key=key, value=value)
    product = vision.types.Product(
        name=product_path,
        product_labels=[key_value])

    # Updating only the product_labels field here.
    update_mask = vision.types.FieldMask(paths=['product_labels'])

    # This overwrites the product_labels.
    updated_product = client.update_product(
        product=product, update_mask=update_mask)

    # Display the updated product information.
    print('Product name: {}'.format(updated_product.name))
    print('Updated product labels: {}'.format(product.product_labels))


def create_reference_image(
        project_id, location, product_id, reference_image_id, gcs_uri):
    """Create a reference image.
    Args:
        project_id: Id of the project.
        location: A compute region name.
        product_id: Id of the product.
        reference_image_id: Id of the reference image.
        gcs_uri: Google Cloud Storage path of the input image.
    """
    client = vision.ProductSearchClient(credentials = credentials)

    # Get the full path of the product.
    product_path = client.product_path(
        project=project_id, location=location, product=product_id)

    # Create a reference image.
    reference_image = vision.types.ReferenceImage(uri=gcs_uri)

    # The response is the reference image with `name` populated.
    image = client.create_reference_image(
        parent=product_path,
        reference_image=reference_image,
        reference_image_id=reference_image_id)

    # Display the reference image information.
    print('Reference image name: {}'.format(image.name))
    print('Reference image uri: {}'.format(image.uri))

def get_similar_products_file(
        project_id, location, product_set_id, product_category,
        file_path, filter):
    """Search similar products to image.
    Args:
        project_id: Id of the project.
        location: A compute region name.
        product_set_id: Id of the product set.
        product_category: Category of the product.
        file_path: Local file path of the image to be searched.
        filter: Condition to be applied on the labels.
        Example for filter: (color = red OR color = blue) AND style = kids
        It will search on all products with the following labels:
        color:red AND style:kids
        color:blue AND style:kids
    """
    # product_search_client is needed only for its helper methods.
    product_search_client = vision.ProductSearchClient(credentials = credentials)
    image_annotator_client = vision.ImageAnnotatorClient(credentials=credentials)

    # Read the image as a stream of bytes.
    with open(file_path, 'rb') as image_file:
        content = image_file.read()
        #print(content)

    # Create annotate image request along with product search feature.
    image = vision.types.Image(content=content)
    #print(image)

    # product search specific parameters
    product_set_path = product_search_client.product_set_path(
        project=project_id, location=location,
        product_set=product_set_id)
    product_search_params = vision.types.ProductSearchParams(
        product_set=product_set_path,
        product_categories=[product_category],
        filter=filter)
    image_context = vision.types.ImageContext(
        product_search_params=product_search_params)

    # Search products similar to the image.
    response = image_annotator_client.product_search(
        image, image_context=image_context)
    #print(response)

    index_time = response.product_search_results.index_time
    #print('Product set index time:')
    #print('  seconds: {}'.format(index_time.seconds))
    #print('  nanos: {}\n'.format(index_time.nanos))

    results = response.product_search_results.results
    #print(results[0].product)

    print('Most Similar Product')
    ans = None
    curr_score = 0
    for result in results:
        #print(ans)
        if result.score > curr_score:
            ans = result
            curr_score = result.score
        
        product = result.product

        print('Score(Confidence): {}'.format(result.score))
        print('Image name: {}'.format(result.image))

        print('Product name: {}'.format(product.name))
        print('Product display name: {}'.format(product.display_name))
        print('Product description: {}\n'.format(product.description))
        print('Product labels: {}\n'.format(product.product_labels))

def list_product_sets(project_id, location):
    """List all product sets.
    Args:
        project_id: Id of the project.
        location: A compute region name.
    """
    client = vision.ProductSearchClient(credentials = credentials)

    # A resource that represents Google Cloud Platform location.
    location_path = client.location_path(
        project=project_id, location=location)

    # List all the product sets available in the region.
    product_sets = client.list_product_sets(parent=location_path)

    # Display the product set information.
    for product_set in product_sets:
        print('Product set name: {}'.format(product_set.name))
        print('Product set id: {}'.format(product_set.name.split('/')[-1]))
        print('Product set display name: {}'.format(product_set.display_name))
        print('Product set index time:')
        print('  seconds: {}'.format(product_set.index_time.seconds))
        print('  nanos: {}\n'.format(product_set.index_time.nanos))
    #print(ans)

def list_products(project_id, location):
    """List all products.
    Args:
        project_id: Id of the project.
        location: A compute region name.
    """
    client = vision.ProductSearchClient(credentials=credentials)

    # A resource that represents Google Cloud Platform location.
    location_path = client.location_path(project=project_id, location=location)

    # List all the products available in the region.
    products = client.list_products(parent=location_path)

    # Display the product information.
    for product in products:
        print('Product name: {}'.format(product.name))
        print('Product id: {}'.format(product.name.split('/')[-1]))
        print('Product display name: {}'.format(product.display_name))
        print('Product description: {}'.format(product.description))
        print('Product category: {}'.format(product.product_category))
        print('Product labels: {}\n'.format(product.product_labels))

def list_reference_images(
        project_id, location, product_id):
    """List all images in a product.
    Args:
        project_id: Id of the project.
        location: A compute region name.
        product_id: Id of the product.
    """
    client = vision.ProductSearchClient(credentials = credentials)

    # Get the full path of the product.
    product_path = client.product_path(
        project=project_id, location=location, product=product_id)

    # List all the reference images available in the product.
    reference_images = client.list_reference_images(parent=product_path)

    # Display the reference image information.
    for image in reference_images:
        print('Reference image name: {}'.format(image.name))
        print('Reference image id: {}'.format(image.name.split('/')[-1]))
        print('Reference image uri: {}'.format(image.uri))
        print('Reference image bounding polygons: {}'.format(
            image.bounding_polys))


#2 product sets created (070319, and 070318)
#create_product_set("outfitgenerator","us-east1","PS_CLOTH-SHOE_070319","CLOTH-SHOE")
#create_product("outfitgenerator","us-east1","PS_CLOTH-SHOE_070319","Blye Dress","apparel")

#Each product has unique id
#create_product("outfitgenerator","us-east1","PS_CLOTH-SHOE_1","Blue Dress","apparel")

#add_product_to_product_set("outfitgenerator","us-east1","PS_CLOTH-SHOE_1","PS_CLOTH-SHOE_070319")
#create_product("outfitgenerator","us-east1","PS_CLOTH-SHOE_1","Blue Dress","apparel")
#update_product_labels("outfitgenerator","us-east1","PS_CLOTH-SHOE_1","style","women")
#update_product_labels("outfitgenerator","us-east1","PS_CLOTH-SHOE_1","category","dress")
#create_reference_image("outfitgenerator","us-east1","PS_CLOTH-SHOE_1","I_469a896b70ba11e8be97d20059124800_070418","gs://clothmatching/demo-img.jpg")
#path = "C:/Users/ahmed/Documents/Summer2019/PersonalWebsite/img/possibleheader.jpg"
#get_similar_products_file("outfitgenerator","us-east1","PS_CLOTH-SHOE_070319", "apparel",path, "category=dress")

#print(os.path.dirname())

#create_product_set("outfitgenerator","us-east1","PS_OUTFITS01","AHMED-OUTFITS")

#Create Products

"""
#create_product("outfitgenerator","us-east1","AHMEDITEM-01","Beige Jacket","apparel")
update_product_labels("outfitgenerator","us-east1","AHMEDITEM-01","category","jackets")

#create_product("outfitgenerator","us-east1","AHMEDITEM-02","Black Jeans","apparel")
update_product_labels("outfitgenerator","us-east1","AHMEDITEM-02","category","jeans")

#create_product("outfitgenerator","us-east1","AHMEDITEM-03","Blue Jeans","apparel")
update_product_labels("outfitgenerator","us-east1","AHMEDITEM-03","category","jeans")

#create_product("outfitgenerator","us-east1","AHMEDITEM-04","Blue Shirt","apparel")
update_product_labels("outfitgenerator","us-east1","AHMEDITEM-04","category","shirts")

#create_product("outfitgenerator","us-east1","AHMEDITEM-05","Brown Shoes","apparel")
update_product_labels("outfitgenerator","us-east1","AHMEDITEM-05","category","shoes")

#create_product("outfitgenerator","us-east1","AHMEDITEM-06","Crew Neck","apparel")
update_product_labels("outfitgenerator","us-east1","AHMEDITEM-06","category","t-shirts")

#create_product("outfitgenerator","us-east1","AHMEDITEM-07","Green Jacket","apparel")
update_product_labels("outfitgenerator","us-east1","AHMEDITEM-07","category","jackets")

#create_product("outfitgenerator","us-east1","AHMEDITEM-08","Nike T Shirt","apparel")
update_product_labels("outfitgenerator","us-east1","AHMEDITEM-08","category","t-shirts")

#create_product("outfitgenerator","us-east1","AHMEDITEM-09","White Shirt","apparel")
update_product_labels("outfitgenerator","us-east1","AHMEDITEM-09","category","shirts")
"""

"""
create_product_set("outfitgenerator","us-east1","PS_OUTFITS-01","AHMED-OUTFITS")

add_product_to_product_set("outfitgenerator","us-east1","AHMEDITEM-01","PS_OUTFITS-01")
add_product_to_product_set("outfitgenerator","us-east1","AHMEDITEM-02","PS_OUTFITS-01")
add_product_to_product_set("outfitgenerator","us-east1","AHMEDITEM-03","PS_OUTFITS-01")
add_product_to_product_set("outfitgenerator","us-east1","AHMEDITEM-04","PS_OUTFITS-01")
add_product_to_product_set("outfitgenerator","us-east1","AHMEDITEM-05","PS_OUTFITS-01")
add_product_to_product_set("outfitgenerator","us-east1","AHMEDITEM-06","PS_OUTFITS-01")
add_product_to_product_set("outfitgenerator","us-east1","AHMEDITEM-07","PS_OUTFITS-01")
add_product_to_product_set("outfitgenerator","us-east1","AHMEDITEM-08","PS_OUTFITS-01")
add_product_to_product_set("outfitgenerator","us-east1","AHMEDITEM-09","PS_OUTFITS-01")

create_reference_image("outfitgenerator","us-east1","AHMEDITEM-01","REFIMAGE_01","gs://clothmatching/OutfitGenPics/beigejacket.jpg")
create_reference_image("outfitgenerator","us-east1","AHMEDITEM-02","REFIMAGE_02","gs://clothmatching/OutfitGenPics/blackjeans.jpg")
create_reference_image("outfitgenerator","us-east1","AHMEDITEM-03","REFIMAGE_03","gs://clothmatching/OutfitGenPics/bluejeans.jpg")
create_reference_image("outfitgenerator","us-east1","AHMEDITEM-04","REFIMAGE_04","gs://clothmatching/OutfitGenPics/blueshirt.jpg")
create_reference_image("outfitgenerator","us-east1","AHMEDITEM-05","REFIMAGE_05","gs://clothmatching/OutfitGenPics/brownshoes.jfif")
create_reference_image("outfitgenerator","us-east1","AHMEDITEM-06","REFIMAGE_06","gs://clothmatching/OutfitGenPics/crewneck.jfif")
create_reference_image("outfitgenerator","us-east1","AHMEDITEM-07","REFIMAGE_07","gs://clothmatching/OutfitGenPics/greenjacket.jpg")
create_reference_image("outfitgenerator","us-east1","AHMEDITEM-08","REFIMAGE_08","gs://clothmatching/OutfitGenPics/niketshirt.jpg")
create_reference_image("outfitgenerator","us-east1","AHMEDITEM-09","REFIMAGE_09","gs://clothmatching/OutfitGenPics/whiteshirt.jpg")
"""



#path = r"C:\Users\ahmed\Documents\Summer2019\OutfitGenerator\media\clothes_pics\bluejeans_Sq7tsC7.jpg"
#get_similar_products_file("outfitgenerator","us-east1","ryan_PS","apparel",path,"category=pants")
#list_product_sets("outfitgenerator","us-east1")
#list_products("outfitgenerator","us-east1")
#list_reference_images("outfitgenerator","us-east1","AHMEDITEM-03")

#Following path works
#path = r"C:\Users\ahmed\Documents\Summer2019\OutfitGenPics\blackjeans.jpg"
#get_similar_products_file("outfitgenerator","us-east1","PS_OUTFITS-01","apparel",path,"category=jeans")

#PS_OUTFTS-01 product set works only for some reason
def add(a,b):
    return a+b

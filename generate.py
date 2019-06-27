from google.cloud import vision
#Use transfer learning and Indico API to generate outfits based on a users wardrobe, and style preferences.
#We will need different types of styles
    #Each type of style will have a variety of outfits
#The model then tries to use items in current wardrobe, to create outfits such as the one in the selected style.

#Input = clothing items from style preference outfits
#Output = clothing item from wardrobe

#Will be using Google Cloud Vision API
    #Require Product Set
    #Require Product
    #Require Reference Image

    #Product set contains all products(user items, possibleitems)
    #Loop through all desired outfits, loop through each item in that outfit, then find similar images
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

    index_time = response.product_search_results.index_time
    print('Product set index time:')
    print('  seconds: {}'.format(index_time.seconds))
    print('  nanos: {}\n'.format(index_time.nanos))

    results = response.product_search_results.results
    print(results)

    print('Search results:')
    for result in results:
        product = result.product

        print('Score(Confidence): {}'.format(result.score))
        print('Image name: {}'.format(result.image))

        print('Product name: {}'.format(product.name))
        print('Product display name: {}'.format(
            product.display_name))
        print('Product description: {}\n'.format(product.description))
        print('Product labels: {}\n'.format(product.product_labels))


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

path = r"C:\Users\ahmed\Documents\Summer2019\OutfitGenPics\blackjeans.jpg"
get_similar_products_file("outfitgenerator","us-east1","PS_OUTFITS-01","apparel",path,"category=jeans")

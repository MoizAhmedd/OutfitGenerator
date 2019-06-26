# OutfitGenerator
Generates outfits based on your wardrobe, and style preferences.

# How it will work
<ul>
  <li> Allow users to add their clothes, which will be stored in a postgres database </li>
  <li> User is asked to choose a style preference </li>
  <li> User then asks program to generate an outfit, the program uses the clothes in the database to generate an outfit based on the style preference. </li>
  <li> If the user dislikes the outfit, they can choose "Dislike Outfit", and the outfit will not be generated again. </li>
</ul>

# Changes/Additions to be made
<ul>
  <li> Create User foreign key for bad outfits model, to make each bad outfit specific to user, since 2 users can have same outfits but one may like it and one may not </li>
</ul>
  

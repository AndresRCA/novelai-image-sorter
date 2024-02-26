# NovelAI Image Metadata Scripts

Meta data extraction scripts for images generated with NovelAI's image generation functionality.

`nai_meta.py` extracts prompt information and other settings from the alpha channel of NAI generated images. The information is stored in a json file called `all_metadata.json`.

## How to use

In order to sort your images, first run the `nai_meta.py` script, to do so move your images into the `input/` folder.

### Does it work for all images?

If the image was generated using NovelAI's image generation functionality, and if these were not altered in any form, the script should be able to extract meta data from them, otherwise the script indicates when it has failed to do so.
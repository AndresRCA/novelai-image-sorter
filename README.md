# NovelAI Image Metadata Scripts

Meta data extraction scripts for images generated with NovelAI's image generation functionality.

`nai_meta.py` extracts prompt information and other settings from the alpha channel of NAI generated images. The information is stored in a json file called `all_metadata.json`.

`nai_sort.py` copies the images in `input/` and sorts them into `output/`.

## How to use

In order to sort your images, these are the steps you must follow:

1. Move the images you wish to sort into the `input/` folder.
2. Run the `nai_meta.py` script, this will provide you with a `all_metadata.json` file which contains all the meta data values for all images.
3. Remove the suffix `.example` from the `tags.py.example` file, and populate the array values with the tags you wish to set for the sorting process, these will be the names of the destinations folders (these tag names don't have to be a perfect match, they only need to be a word that is within a tag in order to identify it, so for example in the case of the tag `monkey_d._luffy`, just adding the value `"luffy"` to the character tag array is enough, granted there aren't any other long tags that also have the string `"luffy"` in it, you get the idea).
    > Disclaimer: The tags you use during sorting will be **mutually exclusive**, what do I mean by this? for example if in your list of tags you have `smile`, and `open_mouth`, the script will try to sort by those images that only have one of those tags, not both of them at the same time. This is in order to avoid duplicate images in multiple folders, which would be the inclusive case where you would end up with the same image that has the tags `smile, open_mouth` in two different folders `smile/` and `open_mouth/`. The same principle will apply to character tags, so as a rule of thumb do try to use unique tags with no correlation to each other, otherwise these images with multiple tags won't know what their sorting destination will be.
4. Run the `nai_sort.py` script and watch as your images get sorted and outputted into the `output/` folder.
    > Don't worry, your images in `input/` won't be moved or altered, in the sorting process they will just be copied over to `output/` in the category they belong to.

As a last note, the sorting process is divided in three parts, character tag based sorting, regular tag base sorting, and finally the unsorted. The priority and order of these batches goes as follow:
1. Characters: defined by `CHARACTER_TAGS`
2. Tags: defined by `TAGS`.
3. Unsorted: all other images that didn't meet any of the criteria above.

> Keyword **mutual exclusivity**: think of it as a XOR operator, in the context of sorting images it means that there needs to be **only one** existing identifying tag in that image in order to sent it to the correct destination, otherwise if an image has multiple identifying tags that exist in `TAGS` or `CHARACTER_TAGS` (depending on the case), the sorting algorithm won't be able to make a decision on where to send the image and will ultimately send it to a `unsorted/` folder.

### General list of advice for effective sorting

* Try to fill the character tag array with as many cases as you can find in your local collection in order to avoid mixed character folders. For instance, in the case an image has multiple characters and you only have one of those characters listed in your character tag array, the image to be sorted will be sent to the folder that contains that character match along with the other characters that are in that image. But if we list each character in the image we make use of the **mutual exclusivity rule** and the image will be sent to the `unsorted/` folder.
* In the case of regular tags, try to use unique tags with no correlation to each other in order to make effective use of the mutual exclusivity rule.

### Does it work for all images?

If the image was generated using NovelAI's image generation functionality, and if these were not altered in any form (...Or not, honestly I'm not sure what makes an image lose its meta data), the script should be able to extract meta data from them, otherwise the script indicates when it has failed to do so and these will end up in the `unsorted/` folder.
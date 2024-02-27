# NovelAI Image Metadata Scripts

Meta data extraction and sorting scripts for images generated with NovelAI's image generation functionality.

`nai_meta.py` recursively extracts prompt information and other settings from the alpha channel of NAI generated images that live in the `input/` folder. The information is stored in a json file called `all_metadata.json`. The contents of this file should look something like this:
```json
{
    "metadata": [
        {
            "Description": "{{character name}}, thumbs up, [artist:artistname], etc",
            "Software": "NovelAI",
            "Source": "Stable Diffusion XL C1E1DE52",
            "Generation time": "12.362822907976806",
            "Comment": {
                "prompt": "{{character name}}, thumbs up, [artist:artistname], etc",
                "steps": 28,
                "height": 1024,
                "width": 1024,
                "scale": 5.0,
                "uncond_scale": 1.0,
                "cfg_rescale": 0.0,
                "seed": 3563546993,
                "n_samples": 1,
                "hide_debug_overlay": false,
                "noise_schedule": "native",
                "legacy_v3_extend": false,
                "sampler": "k_euler",
                "controlnet_strength": 1.0,
                "controlnet_model": null,
                "dynamic_thresholding": false,
                "dynamic_thresholding_percentile": 0.999,
                "dynamic_thresholding_mimic_scale": 10.0,
                "sm": true,
                "sm_dyn": false,
                "skip_cfg_below_sigma": 0.0,
                "lora_unet_weights": null,
                "lora_clip_weights": null,
                "uc": "malformed hands, long neck, long body, extra fingers, dark skin girl, mosaic, bad faces, bad face, bad eyes, bad feet, extra toes, earrings,  censor bar, censor bars,  @_@, glowing eyes, sketch, flat color,  bad shadow, uncoordinated body, unnatural body, fused breasts, bad breasts, eyepatch,",
                "request_type": "PromptGenerateRequest",
                "signed_hash": "some random base64 here"
            },
            "File name": "file_name.png"
        },
        {
            "..."
        }
    ],
    "failed_files": [
        "file_name1.png",
        "file2.jpg",
        "..."
    ]
}
```
`"metadata"` is where the meta data for the images is stored at and `"failed_files"` is where files that didn't have meta data on them or encountered an error during processing are listed.

`nai_sort.py` copies the images in `input/` and sorts them into `output/`. 

## Requirements

* Python v3
* NumPy package

## How to use

In order to sort your images, these are the steps you must follow:

1. Make sure your python environment is prepared, on python v3 install the NumPy package by executing the `pip install numpy` command (I recommend creating a virtual environment beforehand).
1. Move the images you wish to sort into the `input/` folder. It doesn't matter if you include subfolders, `nai_meta.py` will read all images and `nai_sort.py` will sort them.
2. Run the `nai_meta.py` script, this will provide you with a `all_metadata.json` file which contains all the meta data values for all images.
3. Remove the suffix `.example` from the `tags.py.example` file, and populate the array values with the tags you wish to set for the sorting process, these will be the names of the destination folders. These tag names don't have to be a perfect match and are treated as case insensitive, they minimmum requirement is that it should be a word that is within a tag in order to be identifiable, so for example in the case of the tag `monkey d. luffy`, just adding the value `"luffy"` to the `CHARACTER_TAGS` array is enough, granted there aren't any other long tags that also have the string `"luffy"` in them, you get the idea.
    > Disclaimer: The tags you use during sorting will be **mutually exclusive**, what do I mean by this? for example if in your list of tags you have `smile`, and `open mouth`, the script will try to sort by those images that only have one of those tags, not both of them at the same time. This is in order to avoid duplicate images in multiple folders, which would be the inclusive case where you would end up with the same image that has the tags `smile, open mouth` in two different folders `smile/` and `open mouth/`. The same principle will apply to character tags, so as a rule of thumb do try to use unique tags with no correlation to each other, otherwise these images with multiple tags won't know what their sorting destination will be. For more information check the [general list of advice for effective sorting](#general-list-of-advice-for-effective-sorting).
4. Run the `nai_sort.py` script and watch as your images get sorted and outputted into the `output/` folder.
    > Conversely, instead of running each python script separately, you could also run the `run_pipeline.sh` executable to execute both scripts with one command. Just make sure to make the `.sh` file executable first.

As a last note, the sorting process is divided in three parts, character tag based sorting, regular tag base sorting, and finally the unsorted. The priority and order of these batches goes as follow:
1. Characters: defined by `CHARACTER_TAGS`
2. Tags: defined by `TAGS`.
3. Unsorted: all other images that didn't meet any of the criteria above.

> Keyword **mutual exclusivity**: think of it as a XOR operator, in the context of sorting images it means that there needs to be **only one** existing identifying tag in that image in order to sent it to the correct destination, otherwise if an image has multiple identifying tags that exist in `TAGS` or `CHARACTER_TAGS` (depending on the case), the sorting algorithm won't be able to make a decision on where to send the image and will ultimately send it to a `unsorted/` folder.

### General list of advice for effective sorting and caution

* Try to fill the character tag array with as many cases as you can find in your local collection in order to avoid mixed character folders. For instance, in the case an image has multiple characters and you only have one of those characters listed in your character tag array, the image to be sorted will be sent to the folder that contains that character match along with the other characters that are in that image. But if we list each character in the image we make use of the **mutual exclusivity rule** and the image will be sent to the `unsorted/` folder.
* Try to be as complete as possible with your tag names, suppose you want to sort by a tag that contains the word `aqua` in it with the intention of sorting images that have the `aqua hair` tag (or a character with the name `aqua`), if you keep it as just `aqua` then you end up risking not sorting images that have both `aqua hair, aqua eyes` because by the **mutual exclusivity rule** the existence of these two tags that contain the word `aqua` won't allow this image to be sorted.
* In the case of regular tags, try to use unique tags with no correlation to each other in order to make effective use of the mutual exclusivity rule.
* Characters tags and regular tags are not bound to each other by the **mutual exclusivity rule**, they are treated as different batches and a tag in the character tag list won't have an effect on the sorting for the regular tag sort batch, and vice versa.
* In theory the string matching regex should be able to match whole words as well as words that are surrounded by underscores `_`, so if you have various images with the character `luffy` but some of them were prompted in different formats like `monkey d. luffy` or `monkey_d._luffy`, the regex pattern should still be able to pick up both cases so there is no need to add redundant tags cases like these.
* `nai_sort.py` does not copy over files in the `input/` folder that are not images, so it is advised to ONLY put images there, we don't want a mistake where you leave a document mixed in it and delete the contents of `input/` after getting your images sorted in `output/`. The supported image files are `['.png', '.jpg', '.jpeg', '.bmp', '.gif', '.tiff']`.

### Does it work for all images?

If the image was generated using NovelAI's image generation functionality, and if these were not altered in any form (...Or not, honestly I'm not sure what makes an image lose its meta data), the script should be able to extract meta data from them, otherwise the script indicates when it has failed to do so and these will end up in the `output/failed attempts/` folder.
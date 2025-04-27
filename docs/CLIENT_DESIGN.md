# Purpose

The flask application should present the User with a form to input a new sample to be processed by our captioning model.

The sample must include a pet image, and some characteristics to inform the captioning.

The output of the captioning model should be displayed on the webpage, along with the provided image.
In addition, we will use the produced caption + characteristics to create a ChatGPT prompt.
That prompt will generate our 'blurb'.

## Form Requirements

Include the following required fields:

- image
- name
- age
- gender
- breed

below should be optional

- size
- coat
- good_w_children
- good_w_dogs
- good_w_cats
- house_trained
- spayed_neutered

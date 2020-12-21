# Presets of response options

Those files can be used to simplify the generation of new question items if the
response are often the same across items.

## Create a new set of response options

Use the `TEMPLATEValueConstraints.jsonld` file and simply replace the content of
`"choices": [ ... ]` with that of the `"responseOptions": {"choices": [ ... ]}`
in the jsonld file of the items that will use this set of response choices.

Once this is done, make sure that the `"responseOptions"` of those items is set
to point to the correct jsonld.

For more info, see this work in progress documentation:
https://github.com/Remi-Gau/reproschema/blob/remi-documentation/docs/43_tips_to_make_your_life_easier.md#using-presets-response-options

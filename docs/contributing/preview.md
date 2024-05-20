# How to preview

There are 2 ways to visualize the checklist you have created.

## Using the online user interface

You can point the already existing user-interface to the schema of the protocol or the activity you have just created.

If you want to visualize an activity on its own, you can use the [reproschema-ui](https://www.repronim.org/reproschema-ui/#/).
To do that you can point the UI to the **raw** content of this activity.

To get access to the raw content of an activity you must click on the `Raw` button on github once you have opened its page,
[see for example the PHQ-9 acvitiy here](https://github.com/ReproNim/reproschema-library/blob/master/activities/PHQ-9/PHQ9_schema).

This will open this URL:
[https://raw.githubusercontent.com/ReproNim/reproschema-library/master/activities/PHQ-9/PHQ9_schema](https://raw.githubusercontent.com/ReproNim/reproschema-library/master/activities/PHQ-9/PHQ9_schema).

You can then pass the the URL of raw content to the UI using the following
template URL:

```bash
https://www.repronim.org/reproschema-ui/#/activities/0?url=url-to-activity-schema
```

To view a protocol, you can also use the reproschema-ui with the following template URL:

```bash
https://www.repronim.org/reproschema-ui/#/?url=url-to-protocol-schema
```

## Working locally

You can work completely locally by serving a Reproschema and the app locally.

### Serve a protocol / activity

You can use the [ecobidas CLI](setup.md#command-line-interface) to serve a fodler containing the protocols, activities, items...

```bash
ecobidas serve cobidas_schema/schemas/neurovault
```

You should then be able to open a browser at this URL `http://0.0.0.0:8000/`
and get the URL of the protocol or the activity you want to visualize.

For example:

```text
http://0.0.0.0:8000/protocols/neurovault_schema.jsonld
```

### Serving the app

If you want to use serve the app locally on your computer, you will need to install [node.js](https://nodejs.org/en/).
A good way to do this is to use node version manager:
some installation instructions are available on the
[user-interface repository](https://github.com/ReproNim/reproschema-ui#serve-the-app-on-your-computer).

Once you have done that you can launch the app with:

```bash
cd reproschema-ui
npm install # (1)
npm run serve # (2)
```

<!-- ANNOTATIONS START -->
1.  Install the Javascript dependencies
2.  Run the development server locally
<!-- ANNOTATIONS END -->

Open your browser and go to [localhost:8080](localhost:8080).

You can then point the local app to your local serve of the protocol to preview it:

```text
localhost:8080/#/?url=http://0.0.0.0:8000/protocols/neurovault_schema.jsonld
```

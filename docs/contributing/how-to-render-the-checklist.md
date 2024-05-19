# How the checklist is rendered

This part gets a bit more "techy" but we will do our best to guide you through it.

First make sure you are familiar with the structure of this project by reading
the [general organization](./general-organization.md) documentation.

## Making the new schema available to the UI

If the previous step went smoothly you now need to make the newly created files
available on your remote repository on github so that the user-interface can
'see' them. This you can do by committing the files newly created on your local
repository and pushing them the remote.

For example if the schema is hosted on the `neurovault` branch of your `origin`
remote repository, the following should do the trick (assuming that you are
already on the `neurovault` branch of your local repo):

```bash
git add --all
git commit -m 'your commit message'
git push origin neurovault
```

### Rendering the checklist

There are 2 ways to visualize the checklist you have created.

#### Using the online user interface

You can point the already existing user-interface to the schema of the protocol
or the activity you have just created.

If you want to visualize an activity on its own, you can use the
[reproschema-ui](https://www.repronim.org/reproschema-ui/#/). To do that you can
point the UI to the **raw** content of this activity.

To get access to the raw content of an activity you must click on the `Raw`
button on github once you have opened its page,
[see for example the PHQ-9 acvitiy here](https://github.com/ReproNim/reproschema-library/blob/master/activities/PHQ-9/PHQ9_schema).
This will open this URL:
[https://raw.githubusercontent.com/ReproNim/reproschema-library/master/activities/PHQ-9/PHQ9_schema](https://raw.githubusercontent.com/ReproNim/reproschema-library/master/activities/PHQ-9/PHQ9_schema).

You can then pass the the URL of raw content to the UI using the following
template URL:

```bash
https://www.repronim.org/reproschema-ui/#/activities/0?url=url-to-activity-schema
```

To view a protocol, you can also use the reproschema-ui with the following
template URL:

```bash
https://www.repronim.org/reproschema-ui/#/?url=url-to-protocol-schema
```

#### Serving the app locally

If you want to use serve the app locally on your computer, you will need to
install [node.js](https://nodejs.org/en/) (the "backend" version of Javascript).
A good way to do this is to use node version manager: some installation
instructions are available on the
[user-interface repository](https://github.com/ReproNim/reproschema-ui#serve-the-app-on-your-computer).

<!-- TODO Is it possible to point the UI to a local file ? -->

Make sure that that you have set the UI correctly so it will read the schema
from the right repository. This can be be set by modifying its
`reproschema-ui/src/config.js` file (e.g see
[here](https://github.com/ReproNim/reproschema-ui/blob/master/src/config.js)).

Modify the `githubSrc` so that it points to the URL of the schema of your
protocol:

```javascript
module.exports = {
    /* eslint-disable */
    githubSrc:
        "https://raw.githubusercontent.com/your-gtihub-account/your-repository/branch-name/folder/protcol_schema_filename",
    banner: "This is a test",
    assetsPublicPath: "/your-repository/",
    backendServer: null,
    consent: true,
};
```

Once you have done that you can launch the app with:

```bash
npm install # Install the Javascript dependencies
npm run serve # Run the development server locally
```

Open your browser and go to [localhost:8080](localhost:8080)

### View the results

After pushing to github:

```text
https://www.repronim.org/reproschema-ui/#/?url=url-to-protocol-schema

https://www.repronim.org/reproschema-ui/#/activities/0?url=url-to-activity-schema
```

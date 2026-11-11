# MyDigitalWorld

A responsive Vue 3 content editor with Firestore-backed tabs, frames, fields, and image documents.

## Run locally

```sh
npm install
npm run serve
```

Create a production build with `npm run build`; run ESLint with `npm run lint`.

## Firebase

The Firebase web app configuration is in `src/firebase.js`. The app uses Cloud Firestore only; it does not initialize Firebase Storage. Configure Firestore rules for the desired users and protect the project before sharing it. This app does not use Firebase Authentication, so its built-in password screen is only a client-side UI gate and is not server-side access control.

The Firestore structure is:

```text
tabs/{tabId}
  frames/{frameId}
    fields/{fieldId}
  images/{imageId}
```

Field documents contain direct values, key–value pairs, text, or references to image documents. Each image document contains its base64-encoded image bytes and metadata. To stay below Firestore's 1 MiB per-document limit, the app accepts images up to 650 KiB each and up to 10 images per text-and-images field. Firestore has finite free quotas; usage beyond the project's included quotas may require billing.

Firestore security rules must permit the relevant tab, frame, field, and image reads/writes for your intended users. Do not use unrestricted public rules for a deployed app. The Firebase config is public client configuration; it is not an access-control mechanism.

## App behavior

- Create, rename, and delete tabs and frames. Frame creation is separate from field creation.
- Select a frame, then add direct, key–value, or text-and-images fields. Fields can be edited or deleted.
- Add, replace, remove, and zoom images in a text-and-images field.
- The password screen defaults to `Suresh@7989`; set `VUE_APP_LOGIN_PASSWORD` at build time to override it. The session expires after one hour. This client-side password is visible in the browser bundle and must not be treated as authentication.
- Rename and delete controls start locked. Use the edit-lock control in the top bar and the edit password (defaults to `MVS`) to unlock them for the current page session; lock them again at any time. Set `VUE_APP_EDIT_PASSWORD` at build time to override that password. This is also a client-side UI gate, not server-side authorization.
- The sidebar becomes a drawer on narrow screens and can be opened or closed from the top bar.
- Field cards, image grids, key–value editors, and dialogs reflow for narrow mobile screens.
- The field-type menu is positioned against the viewport, opens above or below as space allows, and remains usable inside the scrollable content area.
- Use the theme toggle on the login screen or in the workspace top bar to switch between light and dark themes. The preference is saved in this browser.

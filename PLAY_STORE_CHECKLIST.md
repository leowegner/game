# Play Store submission checklist

This is the list of things you need to do that I (Claude) cannot do for you. Everything I can automate is already done.

## Already done (automated)

- [x] Capacitor Android project (`android/`)
- [x] App ID `com.leowegner.megathonk`, name "Mega Thonk"
- [x] target/compileSdk 34, minSdk 22
- [x] Landscape orientation locked (`sensorLandscape`)
- [x] Release keystore generated at `android/app/megathonk-release.jks`
- [x] Signing config wired in `android/app/build.gradle`
- [x] App icons at all densities (mipmap-mdpi through mipmap-xxxhdpi), legacy + adaptive + round
- [x] Adaptive-icon background color set to match game chrome (#341C54)
- [x] Play Store icon (`store/playstore-icon.png`, 512×512)
- [x] Feature graphic (`store/feature-graphic.png`, 1024×500)
- [x] Six landscape screenshots at 1280×720 (`store/screenshots/`)
- [x] Privacy policy text (`PRIVACY.md`)
- [x] Store listing copy (`store/listing.md`)
- [x] Signed release AAB at `android/app/build/outputs/bundle/release/app-release.aab` (run `npm run android:aab`)

## You must do

### One-time setup
- [ ] **Create a Google Play Developer account.** $25 one-time fee. https://play.google.com/console/signup
- [ ] **Save the keystore password somewhere safe and back up `android/app/megathonk-release.jks`.** The password is in `android/keystore.properties` (gitignored). If both are lost you can never publish an update to this app.
- [ ] **Host the privacy policy publicly.** Convert `PRIVACY.md` to HTML and put it at a stable URL (e.g. add it to your GitHub Pages site). The Play Console requires the URL.

### Per-submission
- [ ] **Create the app in Play Console.** App name "Mega Thonk", default language English (US), category Games → Action, free.
- [ ] **Upload `app-release.aab`** to a new release on the Internal testing track first. Don't go straight to production — internal testing lets you install via a Play link without the 1-2 day review.
- [ ] **Fill the Store listing:**
  - Title, short description, full description (copy from `store/listing.md`)
  - App icon: upload `store/playstore-icon.png`
  - Feature graphic: upload `store/feature-graphic.png`
  - Phone screenshots: upload 2-8 from `store/screenshots/` (the 1280×720 ones qualify as "phone" — Play Store accepts 320–3840 px on either dimension with 16:9-ish aspect)
  - Tablet screenshots: same files work for the 7" and 10" tablet slots
- [ ] **Content rating questionnaire.** Use the answers in `store/listing.md`.
- [ ] **Data safety form.** Tick "no data collected, no data shared".
- [ ] **Target audience.** Pick the age group; "13+" or "Everyone" both work given the content.
- [ ] **Ads declaration.** "No, my app does not contain ads."
- [ ] **App access.** "All functionality available without restrictions."
- [ ] **Government app.** "No."
- [ ] **News app.** "No."
- [ ] **COVID-19 contact tracing.** "No."
- [ ] **Health declaration.** "No."
- [ ] **Privacy policy URL.** Paste the URL where you hosted `PRIVACY.md`.
- [ ] **Submit for review.** Internal testing reviews are usually instant; production reviews take 1-7 days for new apps.

## Updating the app later

When you change anything in `script.js` / `levels.js` / `styles.css` / `index.html` / `sprites/`:

1. Bump `versionCode` in `android/app/build.gradle` (must be a strictly-increasing integer per Play Store) and `versionName` (human-readable).
2. Run `npm run android:aab`.
3. Upload the new AAB to a new release in Play Console.

## Things to fix before going to production (optional but recommended)

- The current debug build has the default Capacitor splash screen. Customise it via `android/app/src/main/res/drawable/splash.png` if you care.
- `versionName` is `0.1.0` — bump to `1.0.0` when you consider it ready.
- Add a screenshot showing the SHOP screen with several upgrades purchased; the auto-generated one has an empty shop. (Edit `scripts/gen_screenshots.mjs` to seed `meta.shop` and `meta.gold` before snapping.)
- Run a real playtest on the actual tablet; touch input behaves a bit differently from desktop Chromium and the joystick deadzone may need tuning.

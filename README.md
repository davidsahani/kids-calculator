## 🧙 Kids-Calculator: A Calculator that shows steps

Kids-Calculator, an exceptional tool designed to enrich the learning experience of young minds. This calculator goes beyond the conventional functionality of traditional calculators, offering a unique feature that sets it apart. With Kids-Calculator, solving basic arithmetic operations (+, -, *, /, %) becomes an interactive and educational journey.

Kids-Calculator takes learning to new heights by showing every step of the calculation process, just like solving problems on paper. This meticulous display of intermediate steps enables children to grasp underlying concepts and develop a deeper understanding of basic arithmetic.

It enhances problem-solving skills, boosts confidence, and transforms math exercises into captivating puzzles, fostering independent learning and empowering young minds. With its step-by-step breakdown, It improves comprehension, identifies errors, and guarantees accurate results.


### Visual Examples: Addition and Division
For a glimpse into Kids-Calculator, take a look at these simple previews:

> A simple arithmetic Addition:

<img src="https://github.com/davidsahani/kids-calculator/blob/main/images/addition-screenshot.png" style="height: 604px; width: 376px;"/>

> A simple arithmetic Division:

<img src="https://github.com/davidsahani/kids-calculator/blob/main/images/division-screenshot.png" style="height: 650px; width: 417px;"/>

These images showcase the intuitive interface and the comprehensive display of calculation steps, providing a clear demonstration of how Kids-Calculator brings math to life.


### Supported Platforms

Kids-Calculator is currently available for the following platforms:

- Android
- Windows

### Release Builds

When it comes to the release builds, here's what you need to know:

- Android:
  - For new arm-based Android devices, we recommend downloading the version ending with `*arm64-v8a.apk.`
  - If the above version is not compatible with your device (indicating a non-arm64 architecture), please use the version ending with `*armeabi-v7a.apk.`
  - Note: If you have a device with a different architecture, building the project yourself is required, as it is not officially supported for testing reasons.

- Windows:
  - For Windows, simply download the zip file ending with `*windows.zip.`


### Known Issues:

**Black Screen Issue**

- Description: The text widget in the app displays a black screen when performing division with certain values on specific Android devices.
- Cause: This issue is a limitation of the kivymd framework's text widget, as it cannot handle the excessive amount of text generated during division.
- Fixability: Unfortunately, this issue cannot be fixed, as it stems from a limitation within the kivymd framework itself.
- Potential Solution: One possible approach is to limit the division calculations to a level where the black screen issue does not occur on the affected device. However, this solution may introduce limitations for other devices and does not guarantee that the issue won't arise on different devices.

Thank you for your understanding regarding these known issues with Kids-Calculator.
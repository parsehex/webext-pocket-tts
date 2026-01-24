from pocket_tts import TTSModel
import scipy.io.wavfile

text = """
While developers enjoy working with components in framework libraries, web components are gaining more interest because they work with HTML and CSS and reduce the need for JavaScript. But they also offer the ability to write custom components, enabling larger internal software estates to keep more control of the look and feel on their pages. After our recent story on Shoelace (soon to be re-named Web Awesome) I thought I would take that library for a spin.

Before we look at Shoelace, let's take a quick look at the level just below it, the Google web component library called Lit.

A Quick Look at Lit

This gives us an idea of how components are constructed. We just want to pick out the basic bits, because this is what Shoelace is built on. We'll just look at the code through the playground here.

All we want to do is make a rating button, which takes a thumbs up (and goes green) or thumbs down (red) and changes the rating accordingly.


You can see that we pull in the JavaScript index.js as a module and use our own defined tag called rating-element. The span defined in style doesn't affect the component because of the isolation of the shadow DOM.

Let's extract the interesting bits from the code.


You can see the import of Lit, and the definition of the RatingElement class extending a LitElement. At the bottom of the file, you can see the registration of the tag as a custom element based on RatingElement.



There is a render method that basically builds the basic element.


So, that is quite a bit of code to do something quite simple, but you do get your own reusable component.


Shoelace

Let's go one layer up and use some Shoelace. Now we get built components.


We will install a Shoelace template that uses the rollup bundler and start from there. The bundler helps to resolve components without lazy loading them from the web. This brings us closer to a standard developer workflow.

First I clone the rollup example template. That will have the right npm packages we need.


Then we install the packages. You may well need to do an npm update too.


And finally, run the project...


And kick up the page on a different shell tab...


This is what you should see...


So how did we get these components to show?

First of all, we state in index.js which components we want to load in the bundle...


So that is where the Shoelace button, input and rating components come from. This leaves the index.html to be very lean...


Note that the index.js the HTML refers to is the one unrolled by rollup and placed in the distribution directory.

Want a dark theme? Just alter the index.html to...


And because we already imported the dark theme in the index.js...


Finally a little bit of interactivity (don't forget to refresh your cache between bigger changes).

Let's add a toast-style alert (one that goes to the corner) to the button and give the toast a duration countdown before switching off.

We include the alert component to index.js...

We place the component in our index.html, replacing the button code...


And some control code back in the index.js, before the end...


And the result is already quite impressive...

(What you can't see is the blue countdown line shrinking at the bottom of the alert)


Conclusion

This is just an introduction to using web components with a library like Shoelace — they need a bit of attention initially, but (like a framework) have a lot of rich content. However, unlike a framework, these are working mainly with HTML and CSS.

To make things easier for React users to transition, every Shoelace component can be available to import as a React component. The downside is that SSR (server-side rendering) is still not suitable with web components. And it is true that custom elements are not quite the same as components; the problems that this might cause are fleshed out here.

But overall, if you are thinking of working in or leading a larger web implementation team, make sure you understand the possible benefits of a web component library.
"""
text = text.strip()

voice = "alba"
# voice = "/Users/user/Downloads/hank-mcderbin_testphrase.wav"

output = "lit-vs-shoelace_article.wav"

tts_model = TTSModel.load_model()
voice_state = tts_model.get_state_for_audio_prompt(voice)
audio = tts_model.generate_audio(voice_state, text)
# Audio is a 1D torch tensor containing PCM data.
scipy.io.wavfile.write(output, tts_model.sample_rate, audio.numpy())

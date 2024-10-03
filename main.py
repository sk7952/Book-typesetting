import os
import streamlit as st
from openai import OpenAI
import json
import nest_asyncio
import asyncio
from playwright.async_api import async_playwright
import PyPDF2
from reportlab.lib.pagesizes import letter, A4
from reportlab.pdfgen import canvas
from pypdf import PdfReader, PdfWriter


def get_response(chapter, font_size, lineheight):
  
  # Set up OpenAI API client
    
  client = OpenAI(api_key = st.secrets["Openai_api"])
  font_size_px = f"{font_size}px"
  line_height_val = str(lineheight)
  max_chars = 37000
  # Set up OpenAI model and prompt
  model="gpt-4o-mini-2024-07-18"
  # Split the chapter into two parts based on character count
  if len(chapter) <= max_chars:
        # If the chapter is within the limit, process normally
        prompt_template = """

You are an expert book formatter.
This is a book chapter. your job is to output a typesetted file (USING HTML) which can be converted to a pdf book. So ensure that this book is formatted beautifully following all rules of formatting books. The book should be able to be read easily in a web browser. Include these features in html:
1. Paragraph Formatting
Indentation: Use a small indent (about 1 em) for the first line of each paragraph, or opt for a larger spacing between paragraphs if not using indentation.
2. Line Length
Optimal Line Length: Aim for 50-75 characters per line (including spaces). Lines that are too long or too short can make reading difficult.
3.Line Spacing (Leading)
Comfortable Reading: The line spacing should be the same as given in the example.
4. Proper margins and spaces. The top and Bottom margin for paragraph tag should be 0.1 and 0.2em.
8. Left and Right margins are minimum so the pdf looks like a book.
7.  Consistency
Uniformity: Maintain consistent styles for similar elements (e.g., headings, captions, and block quotes) throughout the book.
8. format special segments correctly and similarly such as a poetry, quotes or exclamatory expressions etc (use italics ) for them
9. Use various of html tags like heading bold etc wherever suitable but dont use colours for text
Keep this in mind : Left and Right margins are minimum.
10. Do not write anything else like ```html in the response, directly start with the doctype line.
11. No need to bold names and use italics for even single words in sentences that are in other languages like Hindi or spanish.
12. The chapter heading should be centrally aligned and start on one fourth level of the new page with a margin on the top.
13. There should be some additional space between the chapter heading and the first paragraph.

I am giving you a sample chapter and its HTML output for your reference. Your outputs should be in that simialr manner. Absolutely Do not use any text from the example in the output.
    This is the sample book : : Chapter 1 - Charred Dreams / Cigarettes &amp; Serenading
Excerpts from Dhruv&#39;s journal:
I can smell winter in the air
The petals of the rose
I gave you on the last day of July
Fall mercilessly
Remembering your foggy breath
Meandering its way to mine
Through the smoke between us
As we drifted through the city
Hand in hand
Gushing with the blowing August wind
You lit a cigarette
And I smoked with you
Under the warm glow
Of the slipping september sun
Bringing with it an everlasting October

I can smell winter in the air
As November creaks
And a chill runs down my spine
The rose petals shudder
And so do I

- (Seasons &amp; Significance), Dhruv

“At the end of the day, love never goes to waste. We’re put in this world only to love and
learn. Later in life, you’ll look back, and reminisce how you didn’t even realise that through
all this ache and confusion, you were simply getting closer to your destiny. ” Mrs. Malhotra
said to his son as he stumbled home drunk again, in the dead of the night. “I don’t know what
I am doing, Ma!” he slurred. A dishevelled, bearded face, damp with half-dried tears, resting
in his mother’s lap.

A whole goddamn year had passed, but the twenty-one-year-old Dhruv Malhotra continued to
walk deliriously into bars, filling the void she left in his heart with alcohol, cigarettes and the
company of strange women.
The morning after another such bizarre and blurry night, he woke up with a splitting
headache, as his eyes adjusted to the light. When an hour of staring at the ceiling and
drinking two cups of black coffee did him no good, he sat on the floor in his dimly-lit room,
clutching his guitar and his journal close to him, pouring his grief into writing a song, but
even creating new music reminded him of her. How they spent so many afternoons in his
basement studio recording covers of their favourite Coldplay songs, after which she would
drag him to the terrace to smoke a cigarette while watching the sunset, unaware at the time
that just like the memories of her, this carcinogenic habit would be equally hard to get rid of.
To most of his friends and even his parents, he looked almost unrecognisable. A thick beard
covered his gullible boyish charm, making him look jagged and intimidating. He spent most
of his time holed up in his room. The only time he left the house was to hit the gym. His
social circle diminished and his grades began falling quickly.
Less than a year ago, with an innocent face and nicely trimmed hair, Dhruv was everyone’s
favourite. Lead guitarist at the college band, straight As with an impressive academic record,
broad shouldered and tall with a lofty sense of confidence and a sharp wit. He had everything
going for him. Until he met the stunning Anisha Singhania.
She stepped into his life like an uninvited storm. He enjoyed getting soaked in the pouring
rain, but before he knew it, he had been struck by lightning.
In the summer of his pre-final year at engineering college, when he was conducting auditions
for the college band, a tall and attractive girl with chestnut-coloured hair walked up to him.
&quot;Hey, I&#39;m Anisha.&quot; She extended her hand.
&quot;Hi! I’m Dhruv,&quot; he responded softly and shook hands with her. He couldn&#39;t help but notice
the striking manicured nails polished with a deep black color.
&quot;I have heard a lot about you.” she said with a strikingly odd smile.
“Oh is that so?” He appeared visibly embarrassed.
“Yeah I’ve heard people say how you’re the best guitarist this band has seen in years. I sing a
little myself. And I was wondering if I could join the band too.&quot;
&quot;Thank you, that&#39;s very kind of you. You&#39;re welcome to the auditions.&quot;
&quot;Thanks for the warm welcome!” She tilted her head to look at him from another angle. “My
turn is in half an hour, so I thought it&#39;d be a good use of time to get to know one of the finest
seniors in college.&quot;
&quot;That&#39;s really kind of you. I&#39;d love to catch up, but I&#39;m sorry, I need to focus on these
auditions right now.&quot; He shrugged and excused himself.
&quot;No worries. It was nice talking to you.&quot;
&quot;All the best for the audition, Anisha,&quot; he said with a placid smile.

Anisha went back and sat on one of the empty chairs in the opposite corner of the auditorium.
He tried to focus on the auditions, but his gaze sprinted in her direction every few minutes. A
couple of times, she caught him stealing glances at her and returned an alluring smile.
Half an hour later, it was her turn. And for some reason, Dhruv was excited for her
performance. And then as her name was announced, she walked up to the stage, gazing
fixedly at Dhruv, she sang ‘A woman’s worth’ by Alicia Keys.
&quot;You could buy me diamonds
You could buy me pearls
Take me on a cruise around the world
Baby, you know I&#39;m worth it...”
Dhruv was spellbound. Her deep husky voice was sexier than her perfect curves. And up
there, she was literally ‘worth it’.
Back home that night, Dhruv was busy working on a new song with his best friend, Arnav.
Just then his phone vibrated to notify Anisha&#39;s friend request on Facebook.
&quot;Who is it?&quot; Arnav enquired.
&quot;Well remember that girl, Anisha, from the auditions today?&quot;
&quot;Yeah, the hot chick who sang, &#39;A woman’s worth&#39;?&quot;
&#39;Yep. It&#39;s her friend-request.&quot;
&quot;Dude, I saw how she was talking to you. She is totally into you.&quot;
&quot;Well let’s not jump to conclusions. It’s just a friend request.”
“That’s her move.”
“Well she could simply be interested in friendship. But she sure is very hot though.&quot;
&quot;Well for starters, you don&#39;t look like a pig yourself.”
“Way to make a guy feel good about himself.” Dhruv smirked.
“Okay fine. You’re smart and a great musician. And you’re kinda rich too. Bottom line-
you&#39;re quite a catch, so go for it!&quot; Arnav said to him sarcastically while grabbing his phone
from his hands and checking out Anisha&#39;s Facebook profile.
&quot;Well, my parents are rich.” Dhruv said, focusing on the keys of the piano.
Arnav rolled his eyes and continued stalking her profile.
Dhruv looked at him with a slackened expression and accepted the friend request.
In less than five minutes his phone buzzed again. This time it was a message from her. He
opened his phone to a, &quot;Hey! How&#39;re you doing?&quot;
&quot;See? So what happened to Mr Righteous, Let&#39;s not generalise and jump to conclusions&#39;,
Arnav gloated. “Say this to her and I bet she is going to fall harder for you. Save your
intellectual side for her!&quot; He joked.

“As you say, sir!” Dhruv resigned to his friend’s comments.
&quot;Good! Now you have fun with your new and smoking hot endeavours.&quot; Arnav smirked
bidding his goodbye.
&quot;See you tomorrow buddy.” Dhruv shrugged, ignoring Arnav’s remarks and got back to his
phone and checked out Anisha&#39;s profile. Her display picture was a stunning portrait of her
clicked on some exotic beach. She was wearing a pair of cute denim shorts and a bright pink
bralette that intricately exposed a sexy tattoo on her back. It caught Dhruv&#39;s attention before
another message from her popped up on the screen.
&quot;Hey! Are you there?&quot; her message read.
Dhruv opened the chat box to text her back.
&quot;Hey! What&#39;s up?&quot;
&quot;Nothing much. Was listening to some classical jazz.&quot;
&quot;Oh, I love Frank Sinatra. ‘Fly me to the moon’ is such a classic.&quot;
&quot;You do? I thought only girls dig those kinds of songs,&quot; Anisha replied.
&quot;I am a huge fan of Sinatra and a lot of other artists from that time. I think if you&#39;re
passionate about music, then you tend to appreciate good work, irrespective of the genre or
the artist. Besides, those are classics,&quot; Dhruv typed.
&quot;Oh, I think I am talking to a proper musician here.&quot; she added a few blushing emojis.
“Haha come on, you’re embarrassing me.&quot;
&quot;You know what&#39;s better than a passionate musician?&quot;
&quot;What?&quot;
&quot;A modest one.&quot;
&quot;Hahaha! Is that so?&quot;
&quot;Oh, it is so. Anyway, who&#39;s your favourite artist or band?&quot; she asked.
&quot;Umm apart from Sinatra, I am a huge Coldplay fan, but I love Eric Clapton and John Mayer
too.&quot;
&quot;Ahh, ‘Tears in heaven’!&quot;
&quot;Oh, it transports me to another world every time I listen to it. In fact I was planning on
doing a cover on it tomorrow.&quot;
&quot;Really? If you don&#39;t mind, can I join? Like I won&#39;t sing, but I can help, you know?&quot;
&quot;Yeah, sure. That&#39;d be great.&quot;
&quot;Perfect, when and where?&quot;
&quot;Umm… tomorrow, my place, around six?&quot;
&quot;Sounds great. I can&#39;t wait!&quot;


This is the sample HTML : <!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Chapter 1</title>
    <style>
        body {
            font-family: 'Times New Roman', serif;
            font-size: <<fontsize>>;
            line-height: <<lineheight>>;
            text-align: justify;
            margin: 2rem 4rem;
        }

	h1.chapter-heading {
            text-align: center;
            margin-top: 25vh; /* Center the heading vertically on the page */
            margin-bottom: 10rem;
            page-break-before: always; /* Start on a new page */
	}

        p {
            text-indent: 1em;
            margin-bottom: 0.1em;
            margin-top: 0.2em;
        }

        blockquote {
            margin: 1em 2em;
            font-style: italic;
        }

        .poetry {
            margin: 1em 2em;
            font-style: italic;
        }
    </style>
</head>
<body>
    <h1 class="chapter-heading">Chapter 1 - Charred Dreams / Cigarettes &amp; Serenading</h1>
    <p>Excerpts from Dhruv's journal:</p>

    <div class="poetry">
        I can smell winter in the air<br>
        The petals of the rose<br>
        I gave you on the last day of July<br>
        Fall mercilessly<br>
        Remembering your foggy breath<br>
        Meandering its way to mine<br>
        Through the smoke between us<br>
        As we drifted through the city<br>
        Hand in hand<br>
        Gushing with the blowing August wind<br>
        You lit a cigarette<br>
        And I smoked with you<br>
        Under the warm glow<br>
        Of the slipping september sun<br>
        Bringing with it an everlasting October<br>
        <br>
        I can smell winter in the air<br>
        As November creaks<br>
        And a chill runs down my spine<br>
        The rose petals shudder<br>
        And so do I
    </div>

    <p><i>- (Seasons &amp; Significance), Dhruv</i></p>

    <blockquote>
        “At the end of the day, love never goes to waste. We’re put in this world only to love and
        learn. Later in life, you’ll look back, and reminisce how you didn’t even realise that through
        all this ache and confusion, you were simply getting closer to your destiny.” Mrs. Malhotra
        said to his son as he stumbled home drunk again, in the dead of the night. “I don’t know what
        I am doing, Ma!” he slurred. A dishevelled, bearded face, damp with half-dried tears, resting
        in his mother’s lap.
    </blockquote>

    <p>A whole goddamn year had passed, but the twenty-one-year-old Dhruv Malhotra continued to
    walk deliriously into bars, filling the void she left in his heart with alcohol, cigarettes and the
    company of strange women.</p>
    <p>The morning after another such bizarre and blurry night, he woke up with a splitting
    headache, as his eyes adjusted to the light. When an hour of staring at the ceiling and
    drinking two cups of black coffee did him no good, he sat on the floor in his dimly-lit room,
    clutching his guitar and his journal close to him, pouring his grief into writing a song, but
    even creating new music reminded him of her. How they spent so many afternoons in his
    basement studio recording covers of their favourite Coldplay songs, after which she would
    drag him to the terrace to smoke a cigarette while watching the sunset, unaware at the time
    that just like the memories of her, this carcinogenic habit would be equally hard to get rid of.</p>
    <p>To most of his friends and even his parents, he looked almost unrecognisable. A thick beard
    covered his gullible boyish charm, making him look jagged and intimidating. He spent most
    of his time holed up in his room. The only time he left the house was to hit the gym. His
    social circle diminished and his grades began falling quickly.</p>
    <p>Less than a year ago, with an innocent face and nicely trimmed hair, Dhruv was everyone’s
    favourite. Lead guitarist at the college band, straight As with an impressive academic record,
    broad shouldered and tall with a lofty sense of confidence and a sharp wit. He had everything
    going for him. Until he met the stunning Anisha Singhania.</p>
    <p>She stepped into his life like an uninvited storm. He enjoyed getting soaked in the pouring
    rain, but before he knew it, he had been struck by lightning.</p>

    <p>In the summer of his pre-final year at engineering college, when he was conducting auditions
    for the college band, a tall and attractive girl with chestnut-coloured hair walked up to him. </p>
    <p>“Hey, I'm Anisha.” She extended her hand. </p>
    <p>“Hi! I’m Dhruv,” he responded softly and shook hands with her. He couldn't help but notice
    the striking manicured nails polished with a deep black color.</p>
    <p>“I have heard a lot about you.” she said with a strikingly odd smile.</p>
    <p>“Oh is that so?” He appeared visibly embarrassed.</p>
    <p>“Yeah I’ve heard people say how you’re the best guitarist this band has seen in years. I sing a
    little myself. And I was wondering if I could join the band too.”</p>
    <p>“Thank you, that's very kind of you. You're welcome to the auditions.”</p>
    <p>“Thanks for the warm welcome!” She tilted her head to look at him from another angle. “My
    turn is in half an hour, so I thought it'd be a good use of time to get to know one of the finest
    seniors in college.” </p>
    <p>“That's really kind of you. I'd love to catch up, but I'm sorry, I need to focus on these
    auditions right now.” He shrugged and excused himself.</p>
    <p>“No worries. It was nice talking to you.”</p>
    <p>“All the best for the audition, Anisha,” he said with a placid smile.</p>

    <p>Anisha went back and sat on one of the empty chairs in the opposite corner of the auditorium.
    He tried to focus on the auditions, but his gaze sprinted in her direction every few minutes. A
    couple of times, she caught him stealing glances at her and returned an alluring smile. </p>
    <p>Half an hour later, it was her turn. And for some reason, Dhruv was excited for her
    performance. And then as her name was announced, she walked up to the stage, gazing
    fixedly at Dhruv, she sang ‘A woman’s worth’ by Alicia Keys.</p>

    <div class="poetry">
    “You could buy me diamonds<br>
    You could buy me pearls<br>
    Take me on a cruise around the world<br>
    Baby, you know I'm worth it...”
    </div>

    <p>Dhruv was spellbound. Her deep husky voice was sexier than her perfect curves. And up
    there, she was literally ‘worth it’. </p>
    <p>Back home that night, Dhruv was busy working on a new song with his best friend, Arnav.
    Just then his phone vibrated to notify Anisha's friend request on Facebook. </p>
    <p>“Who is it?” Arnav enquired.</p>
    <p>“Well remember that girl, Anisha, from the auditions today?”</p>
    <p>“Yeah, the hot chick who sang, ‘A woman’s worth’?”</p>
    <p>“Yep. It’s her friend-request.”</p>
    <p>“Dude, I saw how she was talking to you. She is totally into you.”</p>
    <p>“Well let’s not jump to conclusions. It’s just a friend request.”</p>
    <p>“That’s her move.”</p>
    <p>“Well she could simply be interested in friendship. But she sure is very hot though.”</p>
    <p>“Well for starters, you don’t look like a pig yourself.”</p>
    <p>“Way to make a guy feel good about himself.” Dhruv smirked.</p>
    <p>“Okay fine. You’re smart and a great musician. And you’re kinda rich too. Bottom line-
    you're quite a catch, so go for it!” Arnav said to him sarcastically while grabbing his phone
    from his hands and checking out Anisha's Facebook profile.  </p>
    <p>“Well, my parents are rich.” Dhruv said, focusing on the keys of the piano.</p>
    <p>Arnav rolled his eyes and continued stalking her profile.</p>
    <p>Dhruv looked at him with a slackened expression and accepted the friend request. </p>
    <p>In less than five minutes his phone buzzed again. This time it was a message from her. He
    opened his phone to a, “Hey! How’re you doing?”</p>
    <p>“See? So what happened to Mr Righteous, Let’s not generalise and jump to conclusions’,
    Arnav gloated. “Say this to her and I bet she is going to fall harder for you. Save your
    intellectual side for her!” He joked.</p>
    <p>“As you say, sir!” Dhruv resigned to his friend’s comments.</p>
    <p>“Good! Now you have fun with your new and smoking hot endeavours.” Arnav smirked
    bidding his goodbye.</p>
    <p>“See you tomorrow buddy.” Dhruv shrugged, ignoring Arnav’s remarks and got back to his
    phone and checked out Anisha's profile. Her display picture was a stunning portrait of her
    clicked on some exotic beach. She was wearing a pair of cute denim shorts and a bright pink
    bralette that intricately exposed a sexy tattoo on her back. It caught Dhruv's attention before
    another message from her popped up on the screen.</p>
    <p>“Hey! Are you there?” her message read.</p>
    <p>Dhruv opened the chat box to text her back. </p>
    <p>“Hey! What’s up?”</p>
    <p>“Nothing much. Was listening to some classical jazz.”</p>
    <p>“Oh, I love Frank Sinatra. ‘Fly me to the moon’ is such a classic.”</p>
    <p>“You do? I thought only girls dig those kinds of songs,” Anisha replied.</p>
    <p>“I am a huge fan of Sinatra and a lot of other artists from that time. I think if you're
    passionate about music, then you tend to appreciate good work, irrespective of the genre or
    the artist. Besides, those are classics,” Dhruv typed.</p>
    <p>“Oh, I think I am talking to a proper musician here.” she added a few blushing emojis.</p>
    <p>“Haha come on, you’re embarrassing me.” </p>
    <p>“You know what's better than a passionate musician?”</p>
    <p>“What?”</p>
    <p>“A modest one.”</p>
    <p>“Hahaha! Is that so?”  </p>
    <p>“Oh, it is so. Anyway, who's your favourite artist or band?” she asked.</p>
    <p>“Umm apart from Sinatra, I am a huge Coldplay fan, but I love Eric Clapton and John Mayer
    too.”</p>
    <p>“Ahh, ‘Tears in heaven’!”</p>
    <p>“Oh, it transports me to another world every time I listen to it. In fact I was planning on
    doing a cover on it tomorrow.”</p>
    <p>“Really? If you don't mind, can I join? Like I won't sing, but I can help, you know?”</p>
    <p>“Yeah, sure. That'd be great.”</p>
    <p>“Perfect, when and where?”</p>
    <p>“Umm… tomorrow, my place, around six?”</p>
    <p>“Sounds great. I can't wait!”</p>
    </body>
    </html>
    Here is the target chapter: <<CHAPTER_TEXT>>
"""
        prompt = prompt_template.replace("<<CHAPTER_TEXT>>", chapter).replace("<<fontsize>>", font_size_px).replace("<<lineheight>>", line_height_val)
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            model=model,
            temperature=0
        )

        response = chat_completion.choices[0].message.content
        return response

  else:
        # If the chapter exceeds the limit, split into two parts
        split_pos = chapter.rfind('.', 0, max_chars)
        first_part = chapter[:split_pos + 1]
        second_part = chapter[split_pos + 1:]

        # Process the first part normally
        prompt_template_1 = """
        You are an expert book formatter.
This is a book chapter. your job is to output a typesetted file (USING HTML) which can be converted to a pdf book. So ensure that this book is formatted beautifully following all rules of formatting books. The book should be able to be read easily in a web browser. Include these features in html:
1. Paragraph Formatting
Indentation: Use a small indent (about 1 em) for the first line of each paragraph, or opt for a larger spacing between paragraphs if not using indentation.
2. Line Length
Optimal Line Length: Aim for 50-75 characters per line (including spaces). Lines that are too long or too short can make reading difficult.
3.Line Spacing (Leading)
Comfortable Reading: The line spacing should be the same as given in the example.
4. Proper margins and spaces. The top and Bottom margin for paragraph tag should be 0.1 and 0.2em.
8. Left and Right margins are minimum so the pdf looks like a book.
7.  Consistency
Uniformity: Maintain consistent styles for similar elements (e.g., headings, captions, and block quotes) throughout the book.
8. format special segments correctly and similarly such as a poetry, quotes or exclamatory expressions etc (use italics ) for them
9. Use various of html tags like heading bold etc wherever suitable but dont use colours for text
Keep this in mind : Left and Right margins are minimum.
10. Do not write anything else like ```html in the response, directly start with the doctype line.
11. No need to bold names and use italics for even single words in sentences that are in other languages like Hindi or spanish.
12. The chapter heading should be centrally aligned and start on one fourth level of the new page with a margin on the top.
13. There should be some additional space between the chapter heading and the first paragraph.

I am giving you a sample chapter and its HTML output for your reference. Your outputs should be in that simialr manner.  Absolutely Do not use any text from the example in the output.
    This is the sample book : : Chapter 1 - Charred Dreams / Cigarettes &amp; Serenading
Excerpts from Dhruv&#39;s journal:
I can smell winter in the air
The petals of the rose
I gave you on the last day of July
Fall mercilessly
Remembering your foggy breath
Meandering its way to mine
Through the smoke between us
As we drifted through the city
Hand in hand
Gushing with the blowing August wind
You lit a cigarette
And I smoked with you
Under the warm glow
Of the slipping september sun
Bringing with it an everlasting October

I can smell winter in the air
As November creaks
And a chill runs down my spine
The rose petals shudder
And so do I

- (Seasons &amp; Significance), Dhruv

“At the end of the day, love never goes to waste. We’re put in this world only to love and
learn. Later in life, you’ll look back, and reminisce how you didn’t even realise that through
all this ache and confusion, you were simply getting closer to your destiny. ” Mrs. Malhotra
said to his son as he stumbled home drunk again, in the dead of the night. “I don’t know what
I am doing, Ma!” he slurred. A dishevelled, bearded face, damp with half-dried tears, resting
in his mother’s lap.

A whole goddamn year had passed, but the twenty-one-year-old Dhruv Malhotra continued to
walk deliriously into bars, filling the void she left in his heart with alcohol, cigarettes and the
company of strange women.
The morning after another such bizarre and blurry night, he woke up with a splitting
headache, as his eyes adjusted to the light. When an hour of staring at the ceiling and
drinking two cups of black coffee did him no good, he sat on the floor in his dimly-lit room,
clutching his guitar and his journal close to him, pouring his grief into writing a song, but
even creating new music reminded him of her. How they spent so many afternoons in his
basement studio recording covers of their favourite Coldplay songs, after which she would
drag him to the terrace to smoke a cigarette while watching the sunset, unaware at the time
that just like the memories of her, this carcinogenic habit would be equally hard to get rid of.
To most of his friends and even his parents, he looked almost unrecognisable. A thick beard
covered his gullible boyish charm, making him look jagged and intimidating. He spent most
of his time holed up in his room. The only time he left the house was to hit the gym. His
social circle diminished and his grades began falling quickly.
Less than a year ago, with an innocent face and nicely trimmed hair, Dhruv was everyone’s
favourite. Lead guitarist at the college band, straight As with an impressive academic record,
broad shouldered and tall with a lofty sense of confidence and a sharp wit. He had everything
going for him. Until he met the stunning Anisha Singhania.
She stepped into his life like an uninvited storm. He enjoyed getting soaked in the pouring
rain, but before he knew it, he had been struck by lightning.
In the summer of his pre-final year at engineering college, when he was conducting auditions
for the college band, a tall and attractive girl with chestnut-coloured hair walked up to him.
&quot;Hey, I&#39;m Anisha.&quot; She extended her hand.
&quot;Hi! I’m Dhruv,&quot; he responded softly and shook hands with her. He couldn&#39;t help but notice
the striking manicured nails polished with a deep black color.
&quot;I have heard a lot about you.” she said with a strikingly odd smile.
“Oh is that so?” He appeared visibly embarrassed.
“Yeah I’ve heard people say how you’re the best guitarist this band has seen in years. I sing a
little myself. And I was wondering if I could join the band too.&quot;
&quot;Thank you, that&#39;s very kind of you. You&#39;re welcome to the auditions.&quot;
&quot;Thanks for the warm welcome!” She tilted her head to look at him from another angle. “My
turn is in half an hour, so I thought it&#39;d be a good use of time to get to know one of the finest
seniors in college.&quot;
&quot;That&#39;s really kind of you. I&#39;d love to catch up, but I&#39;m sorry, I need to focus on these
auditions right now.&quot; He shrugged and excused himself.
&quot;No worries. It was nice talking to you.&quot;
&quot;All the best for the audition, Anisha,&quot; he said with a placid smile.

Anisha went back and sat on one of the empty chairs in the opposite corner of the auditorium.
He tried to focus on the auditions, but his gaze sprinted in her direction every few minutes. A
couple of times, she caught him stealing glances at her and returned an alluring smile.
Half an hour later, it was her turn. And for some reason, Dhruv was excited for her
performance. And then as her name was announced, she walked up to the stage, gazing
fixedly at Dhruv, she sang ‘A woman’s worth’ by Alicia Keys.
&quot;You could buy me diamonds
You could buy me pearls
Take me on a cruise around the world
Baby, you know I&#39;m worth it...”
Dhruv was spellbound. Her deep husky voice was sexier than her perfect curves. And up
there, she was literally ‘worth it’.
Back home that night, Dhruv was busy working on a new song with his best friend, Arnav.
Just then his phone vibrated to notify Anisha&#39;s friend request on Facebook.
&quot;Who is it?&quot; Arnav enquired.
&quot;Well remember that girl, Anisha, from the auditions today?&quot;
&quot;Yeah, the hot chick who sang, &#39;A woman’s worth&#39;?&quot;
&#39;Yep. It&#39;s her friend-request.&quot;
&quot;Dude, I saw how she was talking to you. She is totally into you.&quot;
&quot;Well let’s not jump to conclusions. It’s just a friend request.”
“That’s her move.”
“Well she could simply be interested in friendship. But she sure is very hot though.&quot;
&quot;Well for starters, you don&#39;t look like a pig yourself.”
“Way to make a guy feel good about himself.” Dhruv smirked.
“Okay fine. You’re smart and a great musician. And you’re kinda rich too. Bottom line-
you&#39;re quite a catch, so go for it!&quot; Arnav said to him sarcastically while grabbing his phone
from his hands and checking out Anisha&#39;s Facebook profile.
&quot;Well, my parents are rich.” Dhruv said, focusing on the keys of the piano.
Arnav rolled his eyes and continued stalking her profile.
Dhruv looked at him with a slackened expression and accepted the friend request.
In less than five minutes his phone buzzed again. This time it was a message from her. He
opened his phone to a, &quot;Hey! How&#39;re you doing?&quot;
&quot;See? So what happened to Mr Righteous, Let&#39;s not generalise and jump to conclusions&#39;,
Arnav gloated. “Say this to her and I bet she is going to fall harder for you. Save your
intellectual side for her!&quot; He joked.

“As you say, sir!” Dhruv resigned to his friend’s comments.
&quot;Good! Now you have fun with your new and smoking hot endeavours.&quot; Arnav smirked
bidding his goodbye.
&quot;See you tomorrow buddy.” Dhruv shrugged, ignoring Arnav’s remarks and got back to his
phone and checked out Anisha&#39;s profile. Her display picture was a stunning portrait of her
clicked on some exotic beach. She was wearing a pair of cute denim shorts and a bright pink
bralette that intricately exposed a sexy tattoo on her back. It caught Dhruv&#39;s attention before
another message from her popped up on the screen.
&quot;Hey! Are you there?&quot; her message read.
Dhruv opened the chat box to text her back.
&quot;Hey! What&#39;s up?&quot;
&quot;Nothing much. Was listening to some classical jazz.&quot;
&quot;Oh, I love Frank Sinatra. ‘Fly me to the moon’ is such a classic.&quot;
&quot;You do? I thought only girls dig those kinds of songs,&quot; Anisha replied.
&quot;I am a huge fan of Sinatra and a lot of other artists from that time. I think if you&#39;re
passionate about music, then you tend to appreciate good work, irrespective of the genre or
the artist. Besides, those are classics,&quot; Dhruv typed.
&quot;Oh, I think I am talking to a proper musician here.&quot; she added a few blushing emojis.
“Haha come on, you’re embarrassing me.&quot;
&quot;You know what&#39;s better than a passionate musician?&quot;
&quot;What?&quot;
&quot;A modest one.&quot;
&quot;Hahaha! Is that so?&quot;
&quot;Oh, it is so. Anyway, who&#39;s your favourite artist or band?&quot; she asked.
&quot;Umm apart from Sinatra, I am a huge Coldplay fan, but I love Eric Clapton and John Mayer
too.&quot;
&quot;Ahh, ‘Tears in heaven’!&quot;
&quot;Oh, it transports me to another world every time I listen to it. In fact I was planning on
doing a cover on it tomorrow.&quot;
&quot;Really? If you don&#39;t mind, can I join? Like I won&#39;t sing, but I can help, you know?&quot;
&quot;Yeah, sure. That&#39;d be great.&quot;
&quot;Perfect, when and where?&quot;
&quot;Umm… tomorrow, my place, around six?&quot;
&quot;Sounds great. I can&#39;t wait!&quot;


This is the sample HTML : <!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Chapter 1</title>
    <style>
        body {
            font-family: 'Times New Roman', serif;
            font-size: <<fontsize>>;
            line-height: <<lineheight>>;
            text-align: justify;
            margin: 2rem 4rem;
        }

	h1.chapter-heading {
            text-align: center;
            margin-top: 25vh; /* Center the heading vertically on the page */
            margin-bottom: 10rem;
            page-break-before: always; /* Start on a new page */
	}

        p {
            text-indent: 1em;
            margin-bottom: 0.1em;
            margin-top: 0.2em;
        }

        blockquote {
            margin: 1em 2em;
            font-style: italic;
        }

        .poetry {
            margin: 1em 2em;
            font-style: italic;
        }
    </style>
</head>
<body>
    <h1 class="chapter-heading">Chapter 1 - Charred Dreams / Cigarettes &amp; Serenading</h1>
    <p>Excerpts from Dhruv's journal:</p>

    <div class="poetry">
        I can smell winter in the air<br>
        The petals of the rose<br>
        I gave you on the last day of July<br>
        Fall mercilessly<br>
        Remembering your foggy breath<br>
        Meandering its way to mine<br>
        Through the smoke between us<br>
        As we drifted through the city<br>
        Hand in hand<br>
        Gushing with the blowing August wind<br>
        You lit a cigarette<br>
        And I smoked with you<br>
        Under the warm glow<br>
        Of the slipping september sun<br>
        Bringing with it an everlasting October<br>
        <br>
        I can smell winter in the air<br>
        As November creaks<br>
        And a chill runs down my spine<br>
        The rose petals shudder<br>
        And so do I
    </div>

    <p><i>- (Seasons &amp; Significance), Dhruv</i></p>

    <blockquote>
        “At the end of the day, love never goes to waste. We’re put in this world only to love and
        learn. Later in life, you’ll look back, and reminisce how you didn’t even realise that through
        all this ache and confusion, you were simply getting closer to your destiny.” Mrs. Malhotra
        said to his son as he stumbled home drunk again, in the dead of the night. “I don’t know what
        I am doing, Ma!” he slurred. A dishevelled, bearded face, damp with half-dried tears, resting
        in his mother’s lap.
    </blockquote>

    <p>A whole goddamn year had passed, but the twenty-one-year-old Dhruv Malhotra continued to
    walk deliriously into bars, filling the void she left in his heart with alcohol, cigarettes and the
    company of strange women.</p>
    <p>The morning after another such bizarre and blurry night, he woke up with a splitting
    headache, as his eyes adjusted to the light. When an hour of staring at the ceiling and
    drinking two cups of black coffee did him no good, he sat on the floor in his dimly-lit room,
    clutching his guitar and his journal close to him, pouring his grief into writing a song, but
    even creating new music reminded him of her. How they spent so many afternoons in his
    basement studio recording covers of their favourite Coldplay songs, after which she would
    drag him to the terrace to smoke a cigarette while watching the sunset, unaware at the time
    that just like the memories of her, this carcinogenic habit would be equally hard to get rid of.</p>
    <p>To most of his friends and even his parents, he looked almost unrecognisable. A thick beard
    covered his gullible boyish charm, making him look jagged and intimidating. He spent most
    of his time holed up in his room. The only time he left the house was to hit the gym. His
    social circle diminished and his grades began falling quickly.</p>
    <p>Less than a year ago, with an innocent face and nicely trimmed hair, Dhruv was everyone’s
    favourite. Lead guitarist at the college band, straight As with an impressive academic record,
    broad shouldered and tall with a lofty sense of confidence and a sharp wit. He had everything
    going for him. Until he met the stunning Anisha Singhania.</p>
    <p>She stepped into his life like an uninvited storm. He enjoyed getting soaked in the pouring
    rain, but before he knew it, he had been struck by lightning.</p>

    <p>In the summer of his pre-final year at engineering college, when he was conducting auditions
    for the college band, a tall and attractive girl with chestnut-coloured hair walked up to him. </p>
    <p>“Hey, I'm Anisha.” She extended her hand. </p>
    <p>“Hi! I’m Dhruv,” he responded softly and shook hands with her. He couldn't help but notice
    the striking manicured nails polished with a deep black color.</p>
    <p>“I have heard a lot about you.” she said with a strikingly odd smile.</p>
    <p>“Oh is that so?” He appeared visibly embarrassed.</p>
    <p>“Yeah I’ve heard people say how you’re the best guitarist this band has seen in years. I sing a
    little myself. And I was wondering if I could join the band too.”</p>
    <p>“Thank you, that's very kind of you. You're welcome to the auditions.”</p>
    <p>“Thanks for the warm welcome!” She tilted her head to look at him from another angle. “My
    turn is in half an hour, so I thought it'd be a good use of time to get to know one of the finest
    seniors in college.” </p>
    <p>“That's really kind of you. I'd love to catch up, but I'm sorry, I need to focus on these
    auditions right now.” He shrugged and excused himself.</p>
    <p>“No worries. It was nice talking to you.”</p>
    <p>“All the best for the audition, Anisha,” he said with a placid smile.</p>

    <p>Anisha went back and sat on one of the empty chairs in the opposite corner of the auditorium.
    He tried to focus on the auditions, but his gaze sprinted in her direction every few minutes. A
    couple of times, she caught him stealing glances at her and returned an alluring smile. </p>
    <p>Half an hour later, it was her turn. And for some reason, Dhruv was excited for her
    performance. And then as her name was announced, she walked up to the stage, gazing
    fixedly at Dhruv, she sang ‘A woman’s worth’ by Alicia Keys.</p>

    <div class="poetry">
    “You could buy me diamonds<br>
    You could buy me pearls<br>
    Take me on a cruise around the world<br>
    Baby, you know I'm worth it...”
    </div>

    <p>Dhruv was spellbound. Her deep husky voice was sexier than her perfect curves. And up
    there, she was literally ‘worth it’. </p>
    <p>Back home that night, Dhruv was busy working on a new song with his best friend, Arnav.
    Just then his phone vibrated to notify Anisha's friend request on Facebook. </p>
    <p>“Who is it?” Arnav enquired.</p>
    <p>“Well remember that girl, Anisha, from the auditions today?”</p>
    <p>“Yeah, the hot chick who sang, ‘A woman’s worth’?”</p>
    <p>“Yep. It’s her friend-request.”</p>
    <p>“Dude, I saw how she was talking to you. She is totally into you.”</p>
    <p>“Well let’s not jump to conclusions. It’s just a friend request.”</p>
    <p>“That’s her move.”</p>
    <p>“Well she could simply be interested in friendship. But she sure is very hot though.”</p>
    <p>“Well for starters, you don’t look like a pig yourself.”</p>
    <p>“Way to make a guy feel good about himself.” Dhruv smirked.</p>
    <p>“Okay fine. You’re smart and a great musician. And you’re kinda rich too. Bottom line-
    you're quite a catch, so go for it!” Arnav said to him sarcastically while grabbing his phone
    from his hands and checking out Anisha's Facebook profile.  </p>
    <p>“Well, my parents are rich.” Dhruv said, focusing on the keys of the piano.</p>
    <p>Arnav rolled his eyes and continued stalking her profile.</p>
    <p>Dhruv looked at him with a slackened expression and accepted the friend request. </p>
    <p>In less than five minutes his phone buzzed again. This time it was a message from her. He
    opened his phone to a, “Hey! How’re you doing?”</p>
    <p>“See? So what happened to Mr Righteous, Let’s not generalise and jump to conclusions’,
    Arnav gloated. “Say this to her and I bet she is going to fall harder for you. Save your
    intellectual side for her!” He joked.</p>
    <p>“As you say, sir!” Dhruv resigned to his friend’s comments.</p>
    <p>“Good! Now you have fun with your new and smoking hot endeavours.” Arnav smirked
    bidding his goodbye.</p>
    <p>“See you tomorrow buddy.” Dhruv shrugged, ignoring Arnav’s remarks and got back to his
    phone and checked out Anisha's profile. Her display picture was a stunning portrait of her
    clicked on some exotic beach. She was wearing a pair of cute denim shorts and a bright pink
    bralette that intricately exposed a sexy tattoo on her back. It caught Dhruv's attention before
    another message from her popped up on the screen.</p>
    <p>“Hey! Are you there?” her message read.</p>
    <p>Dhruv opened the chat box to text her back. </p>
    <p>“Hey! What’s up?”</p>
    <p>“Nothing much. Was listening to some classical jazz.”</p>
    <p>“Oh, I love Frank Sinatra. ‘Fly me to the moon’ is such a classic.”</p>
    <p>“You do? I thought only girls dig those kinds of songs,” Anisha replied.</p>
    <p>“I am a huge fan of Sinatra and a lot of other artists from that time. I think if you're
    passionate about music, then you tend to appreciate good work, irrespective of the genre or
    the artist. Besides, those are classics,” Dhruv typed.</p>
    <p>“Oh, I think I am talking to a proper musician here.” she added a few blushing emojis.</p>
    <p>“Haha come on, you’re embarrassing me.” </p>
    <p>“You know what's better than a passionate musician?”</p>
    <p>“What?”</p>
    <p>“A modest one.”</p>
    <p>“Hahaha! Is that so?”  </p>
    <p>“Oh, it is so. Anyway, who's your favourite artist or band?” she asked.</p>
    <p>“Umm apart from Sinatra, I am a huge Coldplay fan, but I love Eric Clapton and John Mayer
    too.”</p>
    <p>“Ahh, ‘Tears in heaven’!”</p>
    <p>“Oh, it transports me to another world every time I listen to it. In fact I was planning on
    doing a cover on it tomorrow.”</p>
    <p>“Really? If you don't mind, can I join? Like I won't sing, but I can help, you know?”</p>
    <p>“Yeah, sure. That'd be great.”</p>
    <p>“Perfect, when and where?”</p>
    <p>“Umm… tomorrow, my place, around six?”</p>
    <p>“Sounds great. I can't wait!”</p>
    </body>
    </html>
    Here is the target chapter: <<CHAPTER_TEXT>>
        """
        prompt_1 = prompt_template_1.replace("<<CHAPTER_TEXT>>", first_part).replace("<<fontsize>>", font_size_px).replace("<<lineheight>>", line_height_val)

        chat_completion_1 = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": prompt_1,
                }
            ],
            model=model,
            temperature=0
        )

        response_1 = chat_completion_1.choices[0].message.content

        # Process the second part with a modified prompt (no HTML headers)
        prompt_template_2 = """
        You are an expert book formatter.
        Continue formatting the book chapter into HTML following the same styles as before. Do not include the <!DOCTYPE html> declaration, <html>, <head>, or <body> tags. Start directly with the paragraph tags and ensure consistency in formatting with the previous part.
        Font size = <<fontsize>>
        Line height = <<lineheight>>
        Include these features in html:
        1. Paragraph Formatting
        Indentation: Use a small indent (about 1 em) for the first line of each paragraph, or opt for a larger spacing between paragraphs if not using indentation.
        2. Line Length
        Optimal Line Length: Aim for 50-75 characters per line (including spaces). Lines that are too long or too short can make reading difficult.
        3.Line Spacing (Leading)
        Comfortable Reading: The line spacing should be the same as given in the example.
        4. Proper margins and spaces. The top and Bottom margin for paragraph tag should be 0.1 and 0.2em.
        8. Left and Right margins are minimum so the pdf looks like a book.
        7.  Consistency
        Uniformity: Maintain consistent styles for similar elements (e.g., headings, captions, and block quotes) throughout the book.
        8. format special segments correctly and similarly such as a poetry, quotes or exclamatory expressions etc (use italics ) for them
        9. Use various of html tags like heading bold etc wherever suitable but dont use colours for text
        Keep this in mind : Left and Right margins are minimum.
        10. Do not write anything else like ```html in the response, directly start with the paragraph tags.
        11. No need to bold names and use italics for even single words in sentences that are in other languages like Hindi or spanish.

        Here is the continuation of the chapter:
        <<CHAPTER_TEXT>>
        """
        prompt_2 = prompt_template_2.replace("<<CHAPTER_TEXT>>", second_part).replace("<<fontsize>>", font_size_px).replace("<<lineheight>>", line_height_val)

        chat_completion_2 = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": prompt_2,
                }
            ],
            model=model,
            temperature=0
        )

        response_2 = chat_completion_2.choices[0].message.content

        # Now, merge the two responses
        # Extract the <body> content from the first response and append the second response

        # Find the closing </body> and </html> tags in the first response
        body_close_index = response_1.rfind("</body>")
        html_close_index = response_1.rfind("</html>")

        if body_close_index != -1:
            # Insert the second response before the closing </body> tag
            merged_html = response_1[:body_close_index] + "\n" + response_2 + "\n" + response_1[body_close_index:]
        elif html_close_index != -1:
            # Insert before </html> if </body> is not found
            merged_html = response_1[:html_close_index] + "\n" + response_2 + "\n" + response_1[html_close_index:]
        else:
            # If no closing tags are found, simply concatenate
            merged_html = response_1 + "\n" + response_2

        return merged_html
	
def save_response(response):
    html_pth = 'neww.html'
    with open(html_pth, 'w', encoding='utf-8') as file:
        file.write(response)
    return html_pth


nest_asyncio.apply()

async def html_to_pdf_with_margins(html_file, output_pdf):
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()

        with open(html_file, 'r', encoding='utf-8') as file:
            html_content = file.read()

        await page.set_content(html_content, wait_until='networkidle')

        pdf_options = {
            'path': output_pdf,
            'format': 'A4',
            'margin': {
                'top': '85px',
                'bottom': '60px',
                'left': '70px',
                'right': '40px'
            },
            'print_background': True
        }

        await page.pdf(**pdf_options)
        await browser.close()

def get_pdf_page_count(pdf_file):
    with open(pdf_file, 'rb') as f:
        reader = PyPDF2.PdfReader(f)
        return len(reader.pages)
    
def create_overlay_pdf(overlay_pdf, total_pages, starting_page_number, book_name, author_name, font, current_position):
    c = canvas.Canvas(overlay_pdf, pagesize=A4)
    width, height = A4

    def draw_header_footer(page_number, position):
        c.setFont(font, 12)

        if page_number == starting_page_number:
            # First page of the chapter: Draw page number at the bottom center
            footer_y = 30  # Adjust this value to match the bottom text's baseline
            c.drawCentredString(width / 2, footer_y, f'{page_number}')
        elif position == "Right":
            # Right-side pages: Draw header on the right and page number at the right
            c.drawCentredString(width / 2, height - 40, book_name)
            c.drawString(width - 84, height - 40, f'{page_number}')  # Adjusted x-coordinate for gap
        elif position == "Left":
            # Left-side pages: Draw header on the left and page number at the left
            c.drawCentredString(width / 2, height - 40, author_name)
            c.drawString(62, height - 40, f'{page_number}')  # Adjusted x-coordinate for gap

    # Create pages for the overlay
    for i in range(total_pages):
        current_page_number = starting_page_number + i  # Continuous page numbering
        draw_header_footer(current_page_number, current_position)

        # Alternate position for the next page
        current_position = "Left" if current_position == "Right" else "Right"

        c.showPage()

    c.save()

    # Return the final position for the next chapter
    return current_position

def overlay_headers_footers(main_pdf, overlay_pdf, output_pdf):
    pdf_writer = PdfWriter()

    # Load the main PDF and the overlay PDF
    with open(main_pdf, 'rb') as main_file, open(overlay_pdf, 'rb') as overlay_file:
        main_pdf_reader = PdfReader(main_file)
        overlay_pdf_reader = PdfReader(overlay_file)

        # Ensure the overlay PDF has the same number of pages as the main PDF
        print(len(overlay_pdf_reader.pages))
        print(len(main_pdf_reader.pages))
        if len(overlay_pdf_reader.pages) != len(main_pdf_reader.pages):
            raise ValueError("The number of pages in the overlay PDF does not match the number of pages in the main PDF.")

        # Overlay headers and footers on each page
        for page_num in range(len(main_pdf_reader.pages)):
            main_page = main_pdf_reader.pages[page_num]
            overlay_page = overlay_pdf_reader.pages[page_num]

            # Merge the overlay onto the main page
            main_page.merge_page(overlay_page)

            pdf_writer.add_page(main_page)

    # Write the combined PDF to the output file
    with open(output_pdf, 'wb') as outfile:
        pdf_writer.write(outfile)

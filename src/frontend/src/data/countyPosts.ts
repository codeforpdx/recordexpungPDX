export interface Post {
  id: string;
  title: string;
  preview: string;
  name?: string;
}

export interface County {
  name: string;
  posts: Post[];
}

const multnomahPosts: Post[] = [
  { id: 'multnomah-1', title: 'FINALLY!!!', preview: 'After 3 years of waiting I finally got my record expunged! I can actually apply for jobs now without that stupid box haunting me. Thank you to everyone who helped!', name: 'Marcus T.' },
  { id: 'multnomah-2', title: 'Got the job!', preview: 'Just wanted to share - got hired at a warehouse last week. First real job in 6 years. This process saved my life, no joke.' },
  { id: 'multnomah-3', title: 'thank you!', preview: 'i dont even know what to say. got my papers today and i cried. thank you.', name: 'Deja' },
  { id: 'multnomah-4', title: 'How long does it take?', preview: 'Filed my petition in January and still waiting. Is this normal? Getting worried here.' },
  { id: 'multnomah-5', title: 'Second chance', preview: "Just signed a lease on an apartment. They actually approved me. Never thought I'd see this day. God bless this program.", name: 'Robert M.' },
  { id: 'multnomah-6', title: 'This process is frustrating', preview: "Been trying to get my paperwork together for months. Why does it have to be so complicated? I just want to move on with my life." },
  { id: 'multnomah-7', title: 'THANK YOU THANK YOU', preview: "Got approved yesterday! After everything I been through this feels like winning the lottery. Now I can see my kids again without their mom using my record against me.", name: 'James' },
  { id: 'multnomah-8', title: 'Anyone use a lawyer?', preview: "Is it worth paying for a lawyer or can I do this myself? Money is tight but I don't want to mess it up." },
  { id: 'multnomah-9', title: 'finally free', preview: 'Record cleared last month. Applied to 15 jobs this week and got 3 interviews already. This is real yall.' },
  { id: 'multnomah-10', title: 'Background check came back clean!', preview: "First background check since my expungement and it came back totally clean. I almost didn't believe it. This actually works!", name: 'Terrance W.' },
  { id: 'multnomah-11', title: 'took long enough', preview: 'Eight months of paperwork and waiting but its done. wish id known about this sooner.' },
  { id: 'multnomah-12', title: 'I GOT MY RIGHTS BACK', preview: 'Went to the range today for the first time in 12 years. Got my 2A rights restored along with my expungement. Feels good man.', name: 'Kevin' },
  { id: 'multnomah-13', title: 'New job new life', preview: "Started my new job today at a hospital. Never thought I'd be able to work in healthcare with my past. So grateful for this opportunity.", name: 'Maria S.' },
  { id: 'multnomah-14', title: 'this sucked', preview: 'whole process was a nightmare honestly but it worked. just be prepared for a lot of waiting and red tape.' },
  { id: 'multnomah-15', title: 'Thank you!!!', preview: 'Just wanted to say thank you to everyone who posts here. Reading your stories gave me hope when I needed it most.', name: 'Angela' },
  { id: 'multnomah-16', title: 'Clean slate', preview: "Officially got my expungement last week. Applied for a promotion at work today. Here's to second chances." }
];

const washingtonPosts: Post[] = [
  { id: 'washington-1', title: 'Finally done!', preview: "Process took forever but my record is finally clear. Already got two job offers. Don't give up!", name: 'Chris P.' },
  { id: 'washington-2', title: 'thank you all', preview: "couldn't have done this without the support here. my family is so proud of me." },
  { id: 'washington-3', title: 'Got approved!', preview: 'Judge signed off on my petition today! I can finally move forward with my life and put the past behind me.', name: 'Sarah' },
  { id: 'washington-4', title: 'Questions about eligibility', preview: "Does anyone know if a Class C felony from 2015 qualifies? I've been clean since then but not sure if I'm eligible." },
  { id: 'washington-5', title: 'Best decision ever', preview: 'Getting my record expunged was the best decision I ever made. I can finally breathe again.' },
  { id: 'washington-6', title: 'New apartment!', preview: 'Signed a lease today. The background check came back clean and they approved me right away. This is life changing.', name: 'DeShawn' },
  { id: 'washington-7', title: 'THANK YOU!!!!', preview: "I don't even have words. After 10 years of being denied housing, denied jobs, denied everything... I'm finally free.", name: 'Michelle R.' },
  { id: 'washington-8', title: 'Job at Intel', preview: 'Just got hired at Intel. Background check cleared. Never thought this would be possible. Thank you Oregon!' },
  { id: 'washington-9', title: 'so grateful', preview: 'got my paperwork yesterday and just sat there staring at it. this is real. im not a felon anymore.' },
  { id: 'washington-10', title: 'Second chances are real', preview: 'Started my new career last week. Making more money than I ever have. This program literally saved my life.', name: 'Tony' },
  { id: 'washington-11', title: 'Long process but worth it', preview: 'Took about 7 months total but my record is clear. Already seeing the benefits. Stay patient everyone!' },
  { id: 'washington-12', title: 'thank you', preview: 'just thank you. thats all.' }
];

const clackamasPosts: Post[] = [
  { id: 'clackamas-1', title: 'I got a job!', preview: "After two years of trying, I finally got hired. They ran a background check and it came back clean. I'm crying happy tears right now!", name: 'Jessica L.' },
  { id: 'clackamas-2', title: 'This changed everything', preview: 'My record getting expunged changed my whole life. New job, new apartment, new start. Forever grateful.' },
  { id: 'clackamas-3', title: 'FINALLY APPROVED', preview: "Judge approved my petition today!!! 8 months of waiting but its DONE. Time to start applying for real jobs.", name: 'Andre' },
  { id: 'clackamas-4', title: 'thank you!', preview: 'wanted to share my success story. got my expungement 3 months ago and just got hired at my dream job. keep fighting yall!' },
  { id: 'clackamas-5', title: 'Clean background check!', preview: "Just got my first clean background check in 15 years. Still can't believe it. This process works!", name: 'Brian K.' },
  { id: 'clackamas-6', title: 'New beginning', preview: "Record cleared last month. Already seeing doors open that were closed for years. Don't lose hope!" },
  { id: 'clackamas-7', title: 'Got my guns back', preview: 'Rights restored, record clear. Took my son shooting this weekend for the first time. Best feeling ever.' },
  { id: 'clackamas-8', title: 'Worth the wait', preview: 'Process was slow and frustrating but totally worth it. My life is completely different now. Stay strong everyone.', name: 'Patricia' }
];

const lanePosts: Post[] = [
  { id: 'lane-1', title: 'Thank you Eugene!', preview: 'Local legal aid helped me through the whole process. Record is cleared and I start my new job next week!', name: 'Linda M.' },
  { id: 'lane-2', title: 'finally...', preview: 'been waiting for this for so long. record is clear. i can finally stop looking over my shoulder.' },
  { id: 'lane-3', title: 'New job at UO!', preview: "Got hired at the University! Background check cleared. Never thought I'd be able to work at a university with my past.", name: 'David' },
  { id: 'lane-4', title: 'Approved!', preview: "Judge signed my order today. This is the best day of my life. I can't stop smiling!" },
  { id: 'lane-5', title: 'THANK YOU!!!', preview: 'To everyone who helped me - THANK YOU. I got my life back. I got my future back. Forever grateful.', name: 'Jasmine' },
  { id: 'lane-6', title: 'Clean slate', preview: 'Record expunged, background check clear, new apartment approved. Feeling blessed.' },
  { id: 'lane-7', title: 'this works!', preview: 'just want ppl to know this actually works. i was skeptical but my record is totally clear now. apply for it!' }
];

const marionPosts: Post[] = [
  { id: 'marion-1', title: 'Got approved in Salem!', preview: 'Filed my petition in March and just got approved! The Salem courthouse was really helpful. So relieved!' },
  { id: 'marion-2', title: 'THANK YOU', preview: "Record is clear. Got a job offer yesterday. I'm crying. Thank you to everyone who supported me through this." },
  { id: 'marion-3', title: 'Finally!', preview: 'After 6 months of waiting my expungement finally came through. Background checks are coming back clean. This is amazing!' },
  { id: 'marion-4', title: 'State job!', preview: 'Got hired by the state of Oregon! Background cleared. Never thought this would happen. Dreams do come true!' },
  { id: 'marion-5', title: 'thank you!', preview: 'life is different now. in a good way. i can actually plan for the future.' },
  { id: 'marion-6', title: 'New start', preview: 'Expungement approved last week. Already got two job interviews lined up. Feeling hopeful for the first time in years.' },
  { id: 'marion-7', title: 'Worth every penny', preview: "Paid a lawyer to help me and it was worth every cent. Process went smooth and now I'm free. Highly recommend getting help if you can afford it." }
];

const jacksonPosts: Post[] = [
  { id: 'jackson-1', title: 'Medford success story', preview: 'Just got my expungement approved! The whole process took about 5 months. Already applying for better jobs. Thank you!' },
  { id: 'jackson-2', title: 'thank you!!!', preview: 'i dont post much but i had to share. got my record cleared and landed a job. life is good.' },
  { id: 'jackson-3', title: 'Finally approved!', preview: 'Judge signed my order yesterday. I can finally move on from my past. This is the best feeling in the world!' },
  { id: 'jackson-4', title: 'New job new life', preview: 'Started my new job last week. Background check cleared without any issues. This program is a miracle.' },
  { id: 'jackson-5', title: 'Clean record!', preview: 'Expungement complete. Background checks coming back clean. I can finally provide for my family properly. Thank you Oregon!' }
];

const deschutesPosts: Post[] = [
  { id: 'deschutes-1', title: 'Bend processing times?', preview: 'Anyone know how long the Deschutes court is taking right now? Filed my petition 4 months ago and still waiting.' },
  { id: 'deschutes-2', title: 'APPROVED!!!', preview: 'Finally got approved! Took 6 months but it happened. Already got a job lined up at a resort. So excited!' },
  { id: 'deschutes-3', title: 'Thank you!', preview: 'Record cleared last month. Life is completely different. I can actually plan for the future now. Grateful beyond words.' },
  { id: 'deschutes-4', title: 'New job in hospitality', preview: "Got hired at a hotel in Bend. Background check came back clean. First decent job I've had in years. This works!" },
  { id: 'deschutes-5', title: 'finally done', preview: 'process took forever but my records clear now. already seeing benefits. dont give up yall.' }
];

const linnPosts: Post[] = [
  { id: 'linn-1', title: 'Albany success!', preview: 'Just got my expungement approved through Linn County. Process was smoother than I expected. Very grateful!' },
  { id: 'linn-2', title: 'Thank you!', preview: 'Record is clear, got a new job, life is moving forward. This community gave me hope when I had none.' },
  { id: 'linn-3', title: 'Finally free', preview: 'Background check came back clean for the first time in 12 years. I almost cried. This is real!' }
];

const douglasPosts: Post[] = [
  { id: 'douglas-1', title: 'Roseburg approval!', preview: 'Got my expungement approved yesterday! So happy I can finally move forward. Thank you to everyone who helped!' },
  { id: 'douglas-2', title: 'New beginning', preview: 'Record cleared. Got hired at a local mill. First time in years I feel like I have a future. Thank you Oregon!' }
];

const yamhillPosts: Post[] = [
  { id: 'yamhill-1', title: 'McMinnville success', preview: 'Process took 5 months but my record is clear! Already got a job offer. So grateful for this second chance!' },
  { id: 'yamhill-2', title: 'thank you', preview: 'expungement came through last week. background check cleared. starting new job monday. life is good.' }
];

export const oregonCounties: County[] = [
  { name: 'Baker', posts: [] },
  { name: 'Benton', posts: [] },
  { name: 'Clackamas', posts: clackamasPosts },
  { name: 'Clatsop', posts: [] },
  { name: 'Columbia', posts: [] },
  { name: 'Coos', posts: [] },
  { name: 'Crook', posts: [] },
  { name: 'Curry', posts: [] },
  { name: 'Deschutes', posts: deschutesPosts },
  { name: 'Douglas', posts: douglasPosts },
  { name: 'Gilliam', posts: [] },
  { name: 'Grant', posts: [] },
  { name: 'Harney', posts: [] },
  { name: 'Hood River', posts: [] },
  { name: 'Jackson', posts: jacksonPosts },
  { name: 'Jefferson', posts: [] },
  { name: 'Josephine', posts: [] },
  { name: 'Klamath', posts: [] },
  { name: 'Lake', posts: [] },
  { name: 'Lane', posts: lanePosts },
  { name: 'Lincoln', posts: [] },
  { name: 'Linn', posts: linnPosts },
  { name: 'Malheur', posts: [] },
  { name: 'Marion', posts: marionPosts },
  { name: 'Morrow', posts: [] },
  { name: 'Multnomah', posts: multnomahPosts },
  { name: 'Polk', posts: [] },
  { name: 'Sherman', posts: [] },
  { name: 'Tillamook', posts: [] },
  { name: 'Umatilla', posts: [] },
  { name: 'Union', posts: [] },
  { name: 'Wallowa', posts: [] },
  { name: 'Wasco', posts: [] },
  { name: 'Washington', posts: washingtonPosts },
  { name: 'Wheeler', posts: [] },
  { name: 'Yamhill', posts: yamhillPosts },
];

import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import time
import threading
import json
import os
import random
import schedule
import requests
import datetime
import pytz
from timezonefinder import TimezoneFinder

tf = TimezoneFinder()

# ----------------- الإعدادات ----------------- #
TOKEN = '8662986628:AAEmpdWwLtDo_uOdssE6qHtjtlaOndt9TEQ'
bot = telebot.TeleBot(TOKEN)
DATA_FILE = 'subscribers.json'
PREFS_FILE = 'user_prefs.json'


# ----------------- البيانات ----------------- #
ATHKAR = [
    "﴿فَٱذۡكُرُونِیۤ أَذۡكُرۡكُمۡ﴾.",
    "«سُبْحَانَ اللهِ».",
    "«الحَمْدُ للهِ».",
    "«لَا إلَهَ إلَّا اللهُ».",
    "«اللهُ أكْبَرُ».",
    "«لَا حَوْلَ وَلَا قُوَّةَ إلَّا بِاللهِ».",
    "«لَا إلَهَ إلَّا أَنْتَ سُبْحَانَكَ إنِّي كُنْتُ مِنَ الظَّالِمِينَ».",
    "«رَبِّ اغْفِرْ لِي وَتُبْ عَلَيَّ إنَّكَ أنْتَ التَّوَّابُ الرَّحِيمُ».",
    "عن شداد بن أوس رضي الله عنهما ،\nعن النبي ﷺ قال :\n\n\"سَيِّدُ الاسْتِغْفَارِ : «اللَّهُمَّ أنْتَ رَبِّي لَا إلَهَ إلَّا أنْتَ ، خَلَقْتَنِي وَأنَا عَبْدُكَ ، وَأنَا عَلَى عَهْدِكَ وَوَعْدِكَ مَا اسْتَطَعْتُ ، أعُوذُ بِكَ مِنْ شَرِّ مَا صَنَعْتُ ، أبُوءُ لَكَ بِنِعْمَتِكَ عَلَيَّ ، وَأبُوءُ لَكَ بِذَنْبِي فَاغْفِرْ لِي ؛ إنَّهُ لَا يَغْفِرُ الذُّنُوبَ إلَّا أنْتَ». مَنْ قَالَهَا بَعْدَ مَا يُصْبِحُ مُوقِنًا بِهَا فَمَاتَ مِنْ يَوْمِهِ كَانَ مِنْ أهْلِ الجَنَّةِ ، وَمَنْ قَالَهَا بَعْدَ مَا يُمْسِي مُوقِنًا بِهَا فَمَاتَ مِنْ لَيْلَتِهِ كَانَ مِنْ أهْلِ الجَنَّةِ\".\n\n[مسند الإمام أحمد].",
    "﴿وَاسْتَغْفِرِ اللهَ إِنَّ اللهَ كَانَ غَفُورًا رَّحِيمًا﴾.\n\n«اللَّهُمَّ إنِّي ظَلَمْتُ نَفْسِي ظُلْمًا كَثِيرًا ، وَلَا يَغْفِرُ الذُّنُوبَ إلَّا أنْتَ ، فَاغْفِرْ لِي مَغْفِرَةً مِنْ عِنْدِكَ وَارْحَمْنِي ؛ إنَّكَ أنْتَ الغَفُورُ الرَّحِيمُ».",
    "﴿وَلَا تُخْزِنِي يَوْمَ يُبْعَثُونَ • يَوْمَ لَا يَنفَعُ مَالٌ وَلَا بَنُونَ • إِلَّا مَنْ أَتَى اللهَ بِقَلْبٍ سَلِيمٍ﴾.\n\n«يَا مُقَلِّبَ القُلُوبِ ثَبِّتْ قُلُوبَنَا عَلَى دِينِكَ ، وَيَا مُصَرِّفَ القُلُوبِ صَرِّفْ قُلُوبَنَا عَلَى طَاعَتِكَ ، أعِنَّا عَلَى ذِكْرِكَ وَشُكْرِكَ وَحُسْنِ عِبَادَتِكَ».",
    "﴿وَقَلِيلٌ مِّنْ عِبَادِيَ الشَّكُورُ﴾.\n\n«اللَّهُمَّ لَكَ الحَمْدُ حَمْدًا كَثِيرًا طَيِّبًا مُبَارَكًا فِيهِ كَمَا يَنْبَغِي لِجَلَالِ وَجْهِكَ وَعَظِيمِ سُلْطَانِكَ حَمْدًا غَيْرَ مَكْفِيٍّ وَلَا مُوَدَّعٍ وَلَا مُسْتَغْنًى عَنْهُ رَبَّنَا».",
    "﴿وَإِنَّ رَبَّكَ لَهُوَ الْعَزِيزُ الرَّحِيمُ﴾.\n\n«اللَّهُمَّ اغْفِرْ لِي خَطِيئَتِي وَجَهْلِي وَإسْرَافِي فِي أمْرِي وَمَا أنْتَ أعْلَمُ بِهِ مِنِّي ، اللَّهُمَّ اغْفِرْ لِي هَزْلِي وَجِدِّي وَخَطَئِي وَعَمْدِي وَكُلُّ ذَلِكَ عِنْدِي ، اللَّهُمَّ اغْفِرْ لِي مَا قَدَّمْتُ وَمَا أخَّرْتُ وَمَا أسْرَرْتُ وَمَا أعْلَنْتُ أنْتَ المُقَدِّمُ وَأنْتَ المُؤَخِّرُ وَأنْتَ عَلَى كُلِّ شَيْءٍ قَدِيرٌ».",
    "«اللَّهُمَّ صَلِّ وَسَلِّمْ عَلَى نَبِيِّنَا مُحَمَّدٍ».",
    "﴿رَبَّنَا آتِنَا فِي الدُّنْيَا حَسَنَةً وَفِي الآخِرَةِ حَسَنَةً وَقِنَا عَذَابَ النَّارِ﴾.",
    "«يَا حَيُّ يَا قَيُّومُ بِرَحْمَتِكَ أَسْتَغِيثُ، أَصْلِحْ لِي شَأْنِي كُلَّهُ وَلَا تَكِلْنِي إِلَى نَفْسِي طَرْفَةَ عَيْنٍ».",
    "«اللَّهُمَّ إنِّي أسألُكَ الهُدَى، والتُّقَى، والعَفَافَ، والغِنَى».",
    "«سُبْحَانَكَ اللَّهُمَّ وَبِحَمْدِكَ، أَشْهَدُ أَنْ لَا إِلَهَ إِلَّا أَنْتَ، أَسْتَغْفِرُكَ وَأَتُوبُ إِلَيْكَ».",
    "«اللَّهُمَّ أعِنِّي عَلَى ذِكْرِكَ، وَشُكْرِكَ، وَحُسْنِ عِبَادَتِكَ».",
    "﴿رَبَّنَا لَا تُزِغْ قُلُوبَنَا بَعْدَ إِذْ هَدَيْتَنَا وَهَبْ لَنَا مِن لَّدُنكَ رَحْمَةً ۚ إِنَّكَ أَنتَ الْوَهَّابُ﴾."
]

AUTHENTIC_HADITHS = [
    {
        "ar": "📌 قال رسول الله ﷺ:\n«من صلَّى عليَّ صلاةً واحدةً، صلَّى اللهُ عليه عَشْرَ صَلَوَاتٍ...»\n📚 صحيح النسائي.",
        "en": "📌 The Messenger of Allah ﷺ said:\n«Whoever sends blessings upon me once, Allah will send blessings upon him tenfold...»\n📚 Sahih An-Nasai.",
        "ku_badini": "📌 پێغەمبەر ﷺ دبێژیت:\n«هەر کەسەکێ جارەکێ سالاڤەتان ل سەر من بدەت، خودێ دێ دەهـ جار صەلەواتان ل سەر وی دەت...»\n📚 سەحیحا نەسائی.",
        "ku_sorani": "📌 پێغەمبەر ﷺ فەرموویەتی:\n«ھەر کەسێک یەک جار سەڵاواتم لەسەر بدات، خوای گەورە دە جار سەڵاواتی لەسەر دەدات...»\n📚 سەحیحی نەسائی."
    },
    {
        "ar": "📌 قال رسول الله ﷺ:\n«كَلِمَتَانِ خَفِيفَتَانِ علَى اللسَانِ، ثَقِيلَتَانِ في المِيزَانِ...»\n📚 متفق عليه.",
        "en": "📌 The Messenger of Allah ﷺ said:\n«Two words are light on the tongue, heavy on the scales...»\n📚 Muttafaqun Alayhi.",
        "ku_badini": "📌 پێغەمبەر ﷺ دبێژیت:\n«دوو پەیڤ ل سەر ئەزمانی د سڤکن، د تەرازیێ دا د گرانن...»\n📚 متفق علیه‌.",
        "ku_sorani": "📌 پێغەمبەر ﷺ فەرموویەتی:\n«دوو وشە لەسەر زمان سووکن، لە تەرازوودا قورسن...»\n📚 متفق علیە."
    },
    {
        "ar": "📌 قال رسول الله ﷺ:\n«لا يُؤْمِنُ أحَدُكُمْ، حتَّى يُحِبَّ لأخِيهِ ما يُحِبُّ لِنَفْسِهِ».\n📚 متفق عليه.",
        "en": "📌 The Messenger of Allah ﷺ said:\n«None of you truly believes until he loves for his brother what he loves for himself.»\n📚 Muttafaqun Alayhi.",
        "ku_badini": "📌 پێغەمبەر ﷺ دبێژیت:\n«کەس ژ وە ژدل باوەر ناکەت، هەتا ئەو تشتێ بۆ خۆ حەز دکەت بۆ برایێ خۆ ژی حەز بکەت.»\n📚 متفق علیه‌.",
        "ku_sorani": "📌 پێغەمبەر ﷺ فەرموویەتی:\n«کەستان باوەڕی تەواو نییە تاوەکو ئەوەی بۆ خۆی پێی خۆشە بۆ براکەشی پێی خۆش بێت.»\n📚 متفق علیە."
    },
    {
        "ar": "📌 قال رسول الله ﷺ:\n«إنَّ الدَّالَّ علَى الخَيْرِ كَفَاعِلِهِ».\n📚 صحيح الترمذي.",
        "en": "📌 The Messenger of Allah ﷺ said:\n«Whoever guides to something good has a reward similar to that of its doer.»\n📚 Sahih At-Tirmidhi.",
        "ku_badini": "📌 پێغەمبەر ﷺ دبێژیت:\n«ئەوێ رێکا باشیێ نیشا خەلکی ددەت، مینا وی یە یێ کو کری.»\n📚 سەحیحا ترمزی.",
        "ku_sorani": "📌 پێغەمبەر ﷺ فەرموویەتی:\n«ئەو کەسەی ڕێنوێنی خەڵک دەکات بۆ خێر، وەک ئەو کەسە وایە کە خێرەکەی کردووە.»\n📚 سەحیحی تورمزی."
    },
    {
        "ar": "📌 قال رسول الله ﷺ:\n«اتَّقِ اللَّهَ حَيْثُمَا كُنْتَ، وأَتْبِعِ السَّيِّئَةَ الحَسَنَةَ تَمْحُهَا...»\n📚 صحيح الترمذي.",
        "en": "📌 The Messenger of Allah ﷺ said:\n«Fear Allah wherever you are, and follow up a bad deed with a good one...»\n📚 Sahih At-Tirmidhi.",
        "ku_badini": "📌 پێغەمبەر ﷺ دبێژیت:\n«تەقوا خودێ بکە ل هەر جهێ تۆ لێ، و ب دووڤ هەر گونەهەکێ دا قەنجیەکێ بکە دا ژێببەت...»\n📚 سەحیحا ترمزی.",
        "ku_sorani": "📌 پێغەمبەر ﷺ فەرموویەتی:\n«لە ھەر کوێیەک بیت لە خوا بترسە، وە بە دوای ھەر تاوانێکدا چاکەیەک بکە تا بیسڕێتەوە...»\n📚 سەحیحی تورمزی."
    }
]

QURANIC_DUAS = [
    "﴿رَبَّنَا آتِنَا فِي الدُّنْيَا حَسَنَةً وَفِي الآخِرَةِ حَسَنَةً وَقِنَا عَذَابَ النَّارِ﴾",
    "﴿رَبَّنَا لَا تُزِغْ قُلُوبَنَا بَعْدَ إِذْ هَدَيْتَنَا وَهَبْ لَنَا مِن لَّدُنكَ رَحْمَةً ۚ إِنَّكَ أَنتَ الْوَهَّابُ﴾",
    "﴿رَبِّ اجْعَلْنِي مُقِيمَ الصَّلَاةِ وَمِن ذُرِّيَّتِي ۚ رَبَّنَا وَتَقَبَّلْ دُعَاءِ﴾",
    "﴿رَبَّنَا اغْفِرْ لِي وَلِوَالِدَيَّ وَلِلْمُؤْمِنِينَ يَوْمَ يَقُومُ الْحِسَابُ﴾",
    "﴿رَّبِّ أَدْخِلْنِي مُدْخَلَ صِدْقٍ وَأَخْرِجْنِي مُخْرَجَ صِدْقٍ وَاجْعَل لِّي مِن لَّدُنكَ سُلْطَانًا نَّصِيرًا﴾"
]

VIRTUES_OF_ATHKAR = [
    {
        "ar": "🌟 **فضل الذكر:**\nقال رسول الله ﷺ: «مَثَلُ الذي يَذْكُرُ رَبَّهُ والذي لا يَذْكُرُ رَبَّهُ، مَثَلُ الحَيِّ والمَيِّتِ».\n📚 صحيح البخاري.",
        "en": "🌟 **Virtue of Remembering Allah:**\nThe Messenger of Allah ﷺ said: «The example of the one who remembers his Lord in comparison to the one who does not remember his Lord, is that of a living creature compared to a dead one.»\n📚 Sahih al-Bukhari.",
        "ku_badini": "🌟 **خێر و فەزلێ زکری:**\nپێغەمبەر ﷺ دبێژیت: «نموونەیا وی کەسێ زکرێ خودێ دکەت ل گەل وی یێ زکرێ خودێ ناکەت، وەکی نموونەیا کەسێ ساخ و کەسێ مری یە».\n📚 سەحیحا بوخاری.",
        "ku_sorani": "🌟 **خێر و فەزڵی زیکر:**\nپێغەمبەر ﷺ فەرموویەتی: «نموونەی ئەو کەسەی زیکری خوای گەورە دەکات لەگەڵ ئەو کەسەی زیکری ناکات، وەکو نموونەی مردوو و زیندوو وایە».\n📚 سەحیحی بوخاری."
    },
    {
        "ar": "🌟 **فضل الاستغفار:**\nقال رسول الله ﷺ: «مَن لَزِمَ الاستغفارَ، جَعَلَ اللهُ له مِن كُلِّ هَمٍّ فَرَجًا، ومِن كُلِّ ضِيقٍ مَخرَجًا، ورَزَقَهُ مِن حَيثُ لا يَحتَسِبُ».\n📚 سنن أبي داود.",
        "en": "🌟 **Virtue of Seeking Forgiveness:**\nThe Messenger of Allah ﷺ said: «Whoever constantly seeks forgiveness, Allah will appoint for him a way out of every distress and a relief from every anxiety, and will provide sustenance for him from where he expects not.»\n📚 Sunan Abi Dawud.",
        "ku_badini": "🌟 **فەزلێ ئیستیغفارێ (لێخۆشبوونێ):**\nپێغەمبەر ﷺ دبێژیت: «ئەوێ بەردەوام ئیستیغفارێ بکەت، خودێ دێ ژ هەمی خەم و نەخۆشیان ڕزگار کەت، و دێ ژ جهەکێ کو گومانێ بۆ نابەت ڕزقی دەتێ».\n📚 سونەن ئەبی داود.",
        "ku_sorani": "🌟 **فەزڵی ئیستیغفار کردن:**\nپێغەمبەر ﷺ فەرموویەتی: «هەر کەسێک بەردەوام بێت لەسەر ئیستیغفار، خوای گەورە لە هەموو خەم و تەنگانەیەک ڕزگاری دەکات، و لە جێگایەکەوە ڕزقی دەدات کە بیری لێ نەکردۆتەوە».\n📚 سونەنی ئەبی داود."
    },
    {
        "ar": "🌟 **فضل الصلاة على النبي:**\nقال رسول الله ﷺ: «أَولى النَّاسِ بِي يَومَ القِيامَةِ أَكثَرُهُم عَلَيَّ صَلاةً».\n📚 سنن الترمذي.",
        "en": "🌟 **Virtue of Sending Blessings upon the Prophet:**\nThe Messenger of Allah ﷺ said: «The people who will be nearest to me on the Day of Resurrection will be those who send their blessings on me most frequently.»\n📚 Sunan At-Tirmidhi.",
        "ku_badini": "🌟 **فەزلێ صەلەواتدانێ ل سەر پێغەمبەری:**\nپێغەمبەر ﷺ دبێژیت: «نێزیکترین کەس ل من د ڕۆژا قیامەتێ دا ئەو کەسن یێن پترترین صەلەوات ل سەر من داین».\n📚 سونەن ترمزى.",
        "ku_sorani": "🌟 **فەزڵی سەڵاواتدان لەسەر پێغەمبەر:**\nپێغەمبەر ﷺ فەرموویەتی: «لە ڕۆژی قیامەتدا نزیکترین کەس لێمەوە ئەو کەسانەن کە زۆرترین سەڵاواتیان لەسەر داوم».\n📚 سونەنی تورمزی."
    },
    {
        "ar": "🌟 **فضل سبحان الله وبحمده:**\nقال رسول الله ﷺ: «مَن قالَ: سُبحانَ اللهِ وبِحَمدِهِ، في يَومٍ مِائَةَ مَرَّةٍ، حُطَّت خَطاياهُ، وإن كانَت مِثلَ زَبَدِ البَحرِ».\n📚 متفق عليه.",
        "en": "🌟 **Virtue of saying Subhan-Allah wa bihamdihi:**\nThe Messenger of Allah ﷺ said: «Whoever says, 'Subhan Allah wa bihamdihi,' one hundred times a day, will be forgiven all his sins even if they were as much as the foam of the sea.»\n📚 Muttafaqun Alayhi.",
        "ku_badini": "🌟 **فەزلێ سوبحانەللە و بیحەمدیهی:**\nپێغەمبەر ﷺ دبێژیت: «ئەوێ د ڕۆژەکێ دا سەد جاران بێژیت (سُبْحَانَ اللهِ وَبِحَمْدِهِ)، گونەهێن وی دێ وەرنە ژێبرن، خۆ ئەگەر ب قەدەرا کەفچیێن دەریایێ بن ژی».\n📚 متفق عليه.",
        "ku_sorani": "🌟 **فەزڵی سوبحانەڵڵا و بیحەمدیھی:**\nپێغەمبەر ﷺ فەرموویەتی: «هەر کەسێک لە ڕۆژێکدا سەد جار بڵێت (سُبْحَانَ اللهِ وَبِحَمْدِهِ)، تاوانەکانی دەسڕێتەوە، تەنانەت ئەگەر بە ئەندازەی کەفی دەریایش بن».\n📚 متفق علیە."
    }
]

RAMADAN_HADITHS = [
    {
        "ar": "🌙 **حديث رمضاني:**\nقال رسول الله ﷺ: «مَن صامَ رَمَضانَ إيمانًا واحْتِسابًا غُفِرَ له ما تَقَدَّمَ مِن ذَنْبِهِ».\n📚 متفق عليه.",
        "en": "🌙 **Ramadan Hadith:**\nThe Messenger of Allah ﷺ said: «Whoever fasts Ramadan out of faith and in the hope of reward, his previous sins will be forgiven.»\n📚 Muttafaqun Alayhi.",
        "ku_badini": "🌙 **فەرموودەیەکا ڕەمەزانێ:**\nپێغەمبەر ﷺ دبێژیت: «هەر کەسێ ب باوەری و هێڤیا خێرێ ڕوژیێ بگریت، گونەهێن وی یێن بۆری دێ هێنە غەفراندن».\n📚 متفق علیە.",
        "ku_sorani": "🌙 **فەرموودەیەکی ڕەمەزان:**\nپێغەمبەر ﷺ فەرموویەتی: «هەر کەسێک بە باوەڕ و ئومێدی پاداشتەوە ڕۆژووی ڕەمەزان بگرێت، تاوانەکانی پێشووی بۆ دەسڕێتەوە».\n📚 متفق علیە."
    },
    {
        "ar": "🌙 **حديث رمضاني:**\nقال رسول الله ﷺ: «مَن قامَ لَيْلَةَ القَدْرِ إيمانًا واحْتِسابًا، غُفِرَ له ما تَقَدَّمَ مِن ذَنْبِهِ».\n📚 متفق عليه.",
        "en": "🌙 **Ramadan Hadith:**\nThe Messenger of Allah ﷺ said: «Whoever establishes prayers during the nights of Ramadan faithfully out of sincere faith and hoping to attain Allah's rewards, all his past sins will be forgiven.»\n📚 Muttafaqun Alayhi.",
        "ku_badini": "🌙 **فەرموودەیەکا ڕەمەزانێ:**\nپێغەمبەر ﷺ دبێژیت: «هەر کەسێ شەڤا قەدرێ ب باوەری و هێڤیا خێرێ ڕابیت (نڤێژ بکەت)، گونەهێن وی یێن بۆری دێ هێنە غەفراندن».\n📚 متفق علیە.",
        "ku_sorani": "🌙 **فەرموودەیەکی ڕەمەزان:**\nپێغەمبەر ﷺ فەرموویەتی: «هەر کەسێک شەوی قەدر بە باوەڕ و ئومێدی پاداشتەوە زیندوو بکاتەوە، تاوانەکانی پێشووی بۆ دەسڕێتەوە».\n📚 متفق علیە."
    },
    {
        "ar": "🌙 **حديث رمضاني:**\nقال رسول الله ﷺ: «إذا جاءَ رَمَضانُ فُتِّحَتْ أبْوابُ الجَنَّةِ، وغُلِّقَتْ أبْوابُ النَّارِ، وصُفِّدَتِ الشَّياطِينُ».\n📚 متفق عليه.",
        "en": "🌙 **Ramadan Hadith:**\nThe Messenger of Allah ﷺ said: «When the month of Ramadan starts, the gates of the heaven are opened and the gates of Hell are closed and the devils are chained.»\n📚 Muttafaqun Alayhi.",
        "ku_badini": "🌙 **فەرموودەیەکا ڕەمەزانێ:**\nپێغەمبەر ﷺ دبێژیت: «دەمێ ڕەمەزان دهێت، دەرگەهێن بەهەشتێ دهێنە ڤەکرن، و دەرگەهێن جەهەنەمێ دهێنە گرتن، و شەیتان دهێنە گرێدان».\n📚 متفق علیە.",
        "ku_sorani": "🌙 **فەرموودەیەکی ڕەمەزان:**\nپێغەمبەر ﷺ فەرموویەتی: «کاتێک ڕەمەزان دێت، دەرگاکانی بەهەشت دەکرێنەوە، و دەرگاکانی دۆزەخ دادەخرێن، و شەیتانەکان کۆت دەکرێن».\n📚 متفق علیە."
    }
]

ADHAN_VOICES = {
    "abdulbasit": {"ar": "عبدالباسط عبدالصمد", "en": "Abdulbasit Abdulsamad", "ku": "عەبدولباست"},
    "minshawi": {"ar": "محمد المنشاوي", "en": "Muhammad Al-Minshawi", "ku": "محەممەد مەنشاوی"},
    "luhaidan": {"ar": "محمد اللحيدان", "en": "Muhammad Al-Luhaidan", "ku": "محەممەد لوحێدان"},
    "dosari": {"ar": "ياسر الدوسري", "en": "Yasser Al-Dosari", "ku": "یاسر دۆسەری"},
    "rizgar": {"ar": "رزكار كوردي", "en": "Rizgar Kurdi", "ku": "ڕزگار کوردی"},
    "raad": {"ar": "رعد كوردي", "en": "Raad Kurdi", "ku": "ڕەعد کوردی"},
    "peshawa": {"ar": "بيشوا كوردي", "en": "Peshawa Kurdi", "ku": "پێشەوا کوردی"},
    "jazi": {"ar": "محمد جازي عبدالله", "en": "Muhammad Jazi Abdullah", "ku": "محەممەد جازی عەبدوڵڵا"},
    "qatami": {"ar": "ناصر القطامي", "en": "Nasser Al-Qatami", "ku": "ناسر قەتامی"},
    "idris": {"ar": "إدريس أبكر", "en": "Idris Abkar", "ku": "ئیدریس ئەبکەر"},
    "badr": {"ar": "بدر المنشاوي", "en": "Badr Al-Minshawi", "ku": "بەدر مەنشاوی"}
}

ADHAN_AUDIO_URLS = {
    "abdulbasit": "https://download.quranicaudio.com/adhan/abdul_basit.mp3",
    "minshawi": "https://download.quranicaudio.com/adhan/minshawi.mp3",
    "luhaidan": "https://server8.mp3quran.net/luhaidan/Adhan.mp3",
    "dosari": "https://server11.mp3quran.net/yasser/Adhan.mp3",
    "rizgar": "https://ia800701.us.archive.org/3/items/adhan-kurdi/Rizgar_Kurdi.mp3",
    "raad": "https://ia800701.us.archive.org/3/items/adhan-kurdi/Raad_Kurdi.mp3",
    "peshawa": "https://ia800701.us.archive.org/3/items/adhan-kurdi/Peshawa_Kurdi.mp3",
    "jazi": "https://ia800701.us.archive.org/3/items/adhan-kurdi/Muhammad_Jazi.mp3",
    "qatami": "https://server6.mp3quran.net/qtm/Adhan.mp3",
    "idris": "https://server6.mp3quran.net/abkr/Adhan.mp3",
    "badr": "https://ia803204.us.archive.org/16/items/AdhxBaderAlminshawi/Adhan_Bader_Alminshawi.mp3"
}

# نصوص الواجهة
UI_TEXTS = {
    "ar": {
        "welcome": "أهلاً بك [{name}] في بوت الأذكار 📿\n\nنحن سعداء بانضمامك إلينا! يمكنك تصفح الأقسام من خلال القائمة السفلية لتجد ما يملأ يومك بالبركة.\n\nبإمكانك تغيير لغتك المفضلة في أي وقت عبر زر تغيير اللغة.\n\nلإيقاف البوت أرسل: /stop",
        "remind_athkar": "🌟 تذكير بذكر الله:",
        "remind_hadith": "📜 حديث شريف:",
        "morning": "🌅 حان وقت صلاة الفجر! جاري إرسال أذكار الصباح...",
        "evening": "🌌 جاري إرسال أذكار المساء...",
        "here_athkar": "🌟 إليك بعض الأذكار:",
        "stopped": "تم إيقاف إرسال الأذكار في هذه المحادثة.",
        "not_registered": "البوت غير مفعل هنا!",
        "lang_saved": "✅ تم حفظ لغتك المفضلة (العربية) بنجاح.",
        "voice_saved": "✅ تم حفظ صوت الأذان بنجاح.",
        "btns": {
            "morning": "🕌 أذكار الصباح",
            "evening": "🌙 أذكار المساء",
            "hadith": "📜 حديث شريف",
            "random": "📿 أذكار منوعة",
            "lang": "🌐 تغيير اللغة",
            "duas": "🤲 أدعية قرآنية",
            "virtues": "🌟 فضل الذكر",
            "voice": "🗣 اختيار صوت الأذان",
            "location": "📍 تحديد موقعي للأذان"
        }
    },
    "en": {
        "welcome": "Welcome [{name}] to the Adhkar Bot 📿\n\nWe are happy to have you! Use the menu below to navigate and fill your day with blessings.\n\n(Supplications will remain in Arabic; only Hadiths and the Bot interface will be translated)\n\nStop the bot: /stop",
        "remind_athkar": "🌟 Remember Allah:",
        "remind_hadith": "📜 Authentic Hadith:",
        "morning": "🌅 It's Fajr time! Morning Adhkar...",
        "evening": "🌌 Evening Adhkar...",
        "here_athkar": "🌟 Here are some Adhkar:",
        "stopped": "The bot has been stopped in this chat.",
        "not_registered": "The bot is not activated here!",
        "lang_saved": "✅ Language preference saved (English).",
        "voice_saved": "✅ Adhan voice preference saved.",
        "btns": {
            "morning": "🕌 Morning Adhkar",
            "evening": "🌙 Evening Adhkar",
            "hadith": "📜 Hadith",
            "random": "📿 Random Adhkar",
            "lang": "🌐 Change Language",
            "duas": "🤲 Quranic Duas",
            "virtues": "🌟 Virtues of Adhkar",
            "voice": "🗣 Choose Adhan Voice",
            "location": "📍 Set my location for Adhan"
        }
    },
    "ku_badini": {
        "welcome": "Bi xêr hatî [{name}] بۆ بوتا ئەزکاران 📿\n\nئەم دکەیفخۆشین ب هاتنا تە! دشێی ب ڕێیا ڤێ لیستا ل خوارێ هندەک پێزانین و ئەزکارێن خێرێ وەربگری داکو ڕۆژا تە یا پر بەرەکەت بیت.\n\n(دوعا دێ ب عەرەبی مینن؛ تەنێ فەرموودە و ڕووکارێ بوت دێ هێنە وەرگێڕان)\n\nبۆ ڕاگرتنا بوتی: /stop",
        "remind_athkar": "🌟 بیرخستنەوەیا زکرێ خودێ:",
        "remind_hadith": "📜 فەرموودەیا پێغەمبەری:",
        "morning": "🌅 دەمێ نڤێژا سپێدێ یە! ئەزکارێن سپێدێ...",
        "evening": "🌌 ئەزکارێن ئێڤاری...",
        "here_athkar": "🌟 ئەڤە هژمارەکا ئەزکاران:",
        "stopped": "هنارتنا ئەزکاران بۆ ڤێ چاتێ هاتە ڕاگرتن.",
        "not_registered": "بوت ل ڤێرە نە کارایە!",
        "lang_saved": "✅ زمانێ تە ب سەرکەفتیانە هاتە هەلبژارتن (بادینی).",
        "voice_saved": "✅ دەنگی بانگ هاتە پاراستن.",
        "btns": {
            "morning": "🕌 ئەزکارێن سپێدێ",
            "evening": "🌙 ئەزکارێن ئێڤاری",
            "hadith": "📜 فەرموودە",
            "random": "📿 ئەزکارێن جودا جودا",
            "lang": "🌐 گۆهڕینا زمانێ بوت",
            "duas": "🤲 دوعایێن قورئانێ",
            "virtues": "🌟 خێر و فەزلێ زکری",
            "voice": "🗣 هەلبژارتنا دەنگێ بانگی",
            "location": "📍 جهێ خۆ دیار بکە بۆ بانگی"
        }
    },
    "ku_sorani": {
        "welcome": "بەخێربێیت [{name}] بۆ بۆتی ئەزکار 📿\n\nئێمە دڵخۆشین بە ھاتنت! دەتوانیت لە ڕێگەی لیستی خوارەوە بەشەکان ببینی بۆ ئەوەی ڕۆژەکەت پڕ بەرەکەت بکەیت.\n\n(دوعاکان بە عەرەبی دەمێننەوە؛ تەنیا فەرموودە و ڕووکاری بۆتەکە وەردەگێڕدرێن)\n\nبۆ وەستاندنی بۆتەکە: /stop",
        "remind_athkar": "🌟 بیرخستنەوەی زیکری خوا:",
        "remind_hadith": "📜 فەرموودەی پێغەمبەر:",
        "morning": "🌅 کاتی نوێژی بەیانییە! ئەزکارەکانی بەیانی...",
        "evening": "🌌 ئەزکارەکانی ئێوارە...",
        "here_athkar": "🌟 ئەمانە چەند زیکرێکن:",
        "stopped": "ناردنی ئەزکار لەم چاتەدا وەستێنرا.",
        "not_registered": "بۆتەکە لێرە چالاک نییە!",
        "lang_saved": "✅ زمانەکەت بە سەرکەوتوویی ھەڵبژێردرا (سۆرانی).",
        "voice_saved": "✅ دەنگی بانگ پارێزرا.",
        "btns": {
            "morning": "🕌 ئەزکارەکانی بەیانی",
            "evening": "🌙 ئەزکارەکانی ئێوارە",
            "hadith": "📜 فەرموودە",
            "random": "📿 ئەزکارە جۆراوجۆرەکان",
            "lang": "🌐 گۆڕینی زمانی بۆت",
            "duas": "🤲 دۆعاکانی قورئان",
            "virtues": "🌟 خێر و فەزڵی زیکر",
            "voice": "🗣 هەڵبژاردنی دەنگی بانگ",
            "location": "📍 شوێنەکەم دیاری بکە بۆ بانگ"
        }
    }
}

SPECIFIC_ATHKAR = (
    "﴿فَٱذۡكُرُونِیۤ أَذۡكُرۡكُمۡ﴾.\n\n"
    "- «سُبْحَانَ اللهِ».\n"
    "- «الحَمْدُ للهِ».\n"
    "- «لَا إلَهَ إلَّا اللهُ».\n"
    "- «اللهُ أكْبَرُ».\n"
    "- «لَا حَوْلَ وَلَا قُوَّةَ إلَّا بِاللهِ».\n"
    "- «لَا إلَهَ إلَّا أَنْتَ سُبْحَانَكَ إنِّي كُنْتُ مِنَ الظَّالِمِينَ».\n"
    "- «رَبِّ اغْفِرْ لِي وَتُبْ عَلَيَّ إنَّكَ أنْتَ التَّوَّابُ الرَّحِيمُ»."
)

MORNING_ATHKAR = (
    "🌅 أذكار الصباح:\n\n"
    "1. آية الكرسي\n"
    "2. سور الإخلاص والفلق والناس (3 مرات)\n"
    "3. أصبحنا وأصبح الملك لله والحمد لله، لا إله إلا الله وحده لا شريك له، له الملك وله الحمد وهو على كل شيء قدير...\n"
    "4. اللهم بك أصبحنا وبك أمسينا وبك نحيا وبك نموت وإليك النشور.\n"
    "5. رضينا بالله رباً، وبالإسلام ديناً، وبمحمد صلى الله عليه وسلم نبياً (3 مرات)."
)

EVENING_ATHKAR = (
    "🌌 أذكار المساء:\n\n"
    "1. آية الكرسي\n"
    "2. سور الإخلاص والفلق والناس (3 مرات)\n"
    "3. أمسينا وأمسى الملك لله والحمد لله، لا إله إلا الله وحده لا شريك له، له الملك وله الحمد وهو على كل شيء قدير...\n"
    "4. اللهم بك أمسينا وبك أصبحنا وبك نحيا وبك نموت وإليك المصير.\n"
    "5. رضينا بالله رباً، وبالإسلام ديناً، وبمحمد صلى الله عليه وسلم نبياً (3 مرات)."
)

# ----------------- دوال حفظ البيانات ----------------- #
def load_json(file_path, default=None):
    if default is None:
        default = [] if file_path == DATA_FILE else {}
    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return default
    return default

def save_json(data, file_path):
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False)

def add_subscriber(chat_id):
    subs = load_json(DATA_FILE)
    if chat_id not in subs:
        subs.append(chat_id)
        save_json(subs, DATA_FILE)
        return True
    return False

def remove_subscriber(chat_id):
    subs = load_json(DATA_FILE)
    if chat_id in subs:
        subs.remove(chat_id)
        save_json(subs, DATA_FILE)
        return True
    return False

def get_user_lang(chat_id):
    prefs = load_json(PREFS_FILE, {})
    user_data = prefs.get(str(chat_id), {})
    if isinstance(user_data, str):
        # Migration from old format where prefs only stored language string
        return user_data
    return user_data.get("lang", "ku_badini")

def set_user_lang(chat_id, lang):
    prefs = load_json(PREFS_FILE, {})
    if str(chat_id) not in prefs or isinstance(prefs[str(chat_id)], str):
        prefs[str(chat_id)] = {}
    prefs[str(chat_id)]["lang"] = lang
    save_json(prefs, PREFS_FILE)

def set_user_location(chat_id, lat, lon):
    prefs = load_json(PREFS_FILE, {})
    if str(chat_id) not in prefs or isinstance(prefs[str(chat_id)], str):
        prefs[str(chat_id)] = {"lang": "ku_badini"}
    
    prefs[str(chat_id)]["lat"] = lat
    prefs[str(chat_id)]["lon"] = lon
    
    try:
        timezone_str = tf.timezone_at(lng=lon, lat=lat)
        if timezone_str:
            prefs[str(chat_id)]["timezone"] = timezone_str
    except Exception as e:
        print(f"Timezone resolution failed: {e}")
        
    save_json(prefs, PREFS_FILE)

# ----------------- الإرسال التلقائي والقوائم ----------------- #
from telebot.types import ReplyKeyboardMarkup, KeyboardButton

def get_main_menu(lang):
    """إنشاء القائمة السفلية بناءً على لغة المستخدم"""
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    btns = UI_TEXTS[lang]["btns"]
    
    markup.add(
        KeyboardButton(btns["morning"]),
        KeyboardButton(btns["evening"])
    )
    markup.add(
        KeyboardButton(btns["hadith"]),
        KeyboardButton(btns["random"])
    )
    markup.add(
        KeyboardButton(btns["duas"]),
        KeyboardButton(btns["virtues"])
    )
    markup.add(
        KeyboardButton(btns["lang"]),
        KeyboardButton(btns["voice"])
    )
    markup.add(
        KeyboardButton(text=btns["location"], request_location=True)
    )
    return markup
def get_voice_markup(lang):
    markup = InlineKeyboardMarkup()
    buttons = []
    for key, names in ADHAN_VOICES.items():
        name = names["en"] if lang == "en" else (names["ku"] if "ku" in lang else names["ar"])
        buttons.append(InlineKeyboardButton(name, callback_data=f'voice_{key}'))
    
    for i in range(0, len(buttons), 2):
        if i + 1 < len(buttons):
            markup.add(buttons[i], buttons[i+1])
        else:
            markup.add(buttons[i])
    return markup

@bot.callback_query_handler(func=lambda call: call.data.startswith('voice_'))
def handle_voice_selection(call):
    chat_id = call.message.chat.id
    voice_key = call.data.split('_', 1)[1]
    
    prefs = load_json(PREFS_FILE, {})
    if str(chat_id) not in prefs or isinstance(prefs[str(chat_id)], str):
        prefs[str(chat_id)] = {"lang": "ar"}
    prefs[str(chat_id)]["adhan_voice"] = voice_key
    save_json(prefs, PREFS_FILE)
    
    lang = get_user_lang(chat_id)
    msg = UI_TEXTS.get(lang, UI_TEXTS["ar"]).get("voice_saved", "✅ تم الحفظ")
    
    try:
        bot.answer_callback_query(call.id, msg)
        bot.edit_message_text(chat_id=chat_id, message_id=call.message.message_id, text=msg, reply_markup=None)
    except Exception as e:
        print(f"Failed to answer voice callback: {e}")

def get_language_markup():
    markup = InlineKeyboardMarkup()
    btn1 = InlineKeyboardButton("العربية 🇸🇦", callback_data='lang_ar')
    btn2 = InlineKeyboardButton("English 🇬🇧", callback_data='lang_en')
    btn3 = InlineKeyboardButton("بەهدینی ☀️", callback_data='lang_ku_badini')
    btn4 = InlineKeyboardButton("سۆرانی ☀️", callback_data='lang_ku_sorani')
    markup.add(btn1, btn2)
    markup.add(btn3, btn4)
    return markup

@bot.callback_query_handler(func=lambda call: call.data.startswith('lang_'))
def handle_language_selection(call):
    chat_id = call.message.chat.id
    lang = call.data.split('_', 1)[1]
    set_user_lang(chat_id, lang)
    try:
        bot.answer_callback_query(call.id, UI_TEXTS[lang]["lang_saved"])
    except Exception as e:
        print(f"Failed to answer callback query: {e}")
    
    # Update the message to remove inline keyboard, and send the new Reply Keyboard
    bot.edit_message_text(chat_id=chat_id, message_id=call.message.message_id, text=UI_TEXTS[lang]["lang_saved"], reply_markup=None)
    bot.send_message(chat_id, "تم تحديث القائمة / Menu updated / لیست هاتە نویکرن", reply_markup=get_main_menu(lang))

def send_to_all_custom(msg_type, content_func):
    """دالة مخصصة لإرسال الرسائل بناءً على لغة المستخدم"""
    subscribers = load_json(DATA_FILE)
    for chat_id in subscribers:
        try:
            lang = get_user_lang(chat_id)
            title = UI_TEXTS[lang][msg_type]
            text = content_func(lang)
            bot.send_message(chat_id, f"{title}\n\n{text}")
        except Exception as e:
            print(f"فشل في إرسال الرسالة لـ {chat_id}: {e}")

def get_hadith_for_lang(lang, hadith_obj=None):
    if not hadith_obj:
        hadith_obj = random.choice(AUTHENTIC_HADITHS)
    # الجمع بين النص العربي الأصلي والترجمة للغات الأخرى للتبرك
    if lang == "ar":
        return hadith_obj["ar"]
    return f"{hadith_obj['ar']}\n\n---\n{hadith_obj.get(lang, hadith_obj['en'])}"

def job_cycle():
    """دورة زمنية من 50 دقيقة للرسائل"""
    global cycle_counter
    try:
        if 'cycle_counter' not in globals():
            cycle_counter = 0
            
        now = datetime.datetime.now()
        minute = now.minute
        step = (minute // 10) % 5 
        
        print(f"⏳ الدورة الزمنية الحالية: الخطوة {step} (الدقيقة {minute})...")
        
        # التحقق من توقيت السعودية (مكة المكرمة) لرمضان وليلة القدر
        saudi_tz = pytz.timezone('Asia/Riyadh')
        saudi_now = datetime.datetime.now(saudi_tz)
        is_saudi_night = saudi_now.hour >= 18 or saudi_now.hour < 4
        
        prefs = load_json(PREFS_FILE, {})
        hijri_date = prefs.get('server_hijri_date', {})
        is_ramadan = hijri_date.get('month') == '09'
        is_laylat_qadr_days = is_ramadan and int(hijri_date.get('day', 0)) >= 20
        
        # زيادة التكرار في رمضان وليالي القدر
        if step == 0:
            if is_laylat_qadr_days and is_saudi_night:
                qadr_dua = "اللَّهُمَّ إِنَّكَ عَفُوٌّ تُحِبُّ الْعَفْوَ فَاعْفُ عَنِّي"
                send_to_all_custom("remind_athkar", lambda l: f"🌙 **دعاء ليلة القدر:**\n\n{qadr_dua}")
                print(">> تم إرسال دعاء ليلة القدر (العشر الأواخر - توقيت السعودية).")
            else:
                send_to_all_custom("remind_athkar", lambda l: SPECIFIC_ATHKAR)
                print(">> تم إرسال الذكر المخصص.")
                
        elif step == 1 and is_ramadan:
            selected_hadith = random.choice(RAMADAN_HADITHS)
            send_to_all_custom("remind_hadith", lambda l: get_hadith_for_lang(l, selected_hadith))
            print(">> تم إرسال حديث رمضاني إضافي.")
            
        elif step == 2:
            selected_athkar = random.sample(ATHKAR, min(6, len(ATHKAR)))
            thikr_text = "\n\n 🌿 ━━━ 🌿 ━━━ 🌿 \n\n".join(selected_athkar)
            send_to_all_custom("remind_athkar", lambda l: thikr_text)
            print(">> تم إرسال الـ 6 أذكار.")
            
        elif step == 3:
            selected_hadith = random.choice(RAMADAN_HADITHS) if is_ramadan else random.choice(AUTHENTIC_HADITHS)
            send_to_all_custom("remind_hadith", lambda l: get_hadith_for_lang(l, selected_hadith))
            print(">> تم إرسال الحديث.")
            
        elif step == 4 and is_ramadan and is_laylat_qadr_days and is_saudi_night:
            qadr_dua = "اللَّهُمَّ إِنَّكَ عَفُوٌّ تُحِبُّ الْعَفْوَ فَاعْفُ عَنِّي"
            msg = f"🌙 **تذكير بليلة القدر:**\n\n{qadr_dua}"
            send_to_all_custom("remind_athkar", lambda l: msg)
            print(">> تم إرسال تذكير إضافي لليلة القدر.")
            
    except Exception as e:
        print(f"خطأ في الدورة الزمنية: {e}")

def fetch_current_hijri_date():
    """جلب التاريخ الهجري بتوقيت مكة لمعرفة رمضان والعشر الأواخر"""
    try:
        url = "http://api.aladhan.com/v1/gToH"
        current_date = datetime.datetime.now().strftime("%d-%m-%Y")
        response = requests.get(url, params={"date": current_date})
        data = response.json()
        
        if data["code"] == 200:
            hijri = data["data"]["hijri"]
            prefs = load_json(PREFS_FILE, {})
            prefs['server_hijri_date'] = {
                'day': hijri['day'],
                'month': hijri['month']['number'],
                'year': hijri['year']
            }
            save_json(prefs, PREFS_FILE)
            print(f"✅ تم تحديث التاريخ الهجري: {hijri['day']} / {hijri['month']['en']} / {hijri['year']}")
    except Exception as e:
        print(f"❌ خطأ في جلب التاريخ الهجري: {e}")

def get_fajr_time():
    """جلب وقت صلاة الفجر في مكة المكرمة لليوم الحالي"""
    try:
        # API لجلب أوقات الصلاة لمكة المكرمة
        url = "http://api.aladhan.com/v1/timingsByCity"
        params = {
            "city": "Makkah",
            "country": "Saudi Arabia",
            "method": 4 # Umm Al-Qura University, Makkah
        }
        response = requests.get(url, params=params)
        data = response.json()
        
        if data["code"] == 200:
            fajr_time = data["data"]["timings"]["Fajr"]
            print(f"✅ تم جلب وقت صلاة الفجر اليوم في مكة: {fajr_time}")
            return fajr_time
    except Exception as e:
        print(f"❌ خطأ في جلب وقت الفجر: {e}")
    
    # وقت افتراضي في حال فشل الـ API
    return "05:00"

def cache_adhan_times_for_all_users():
    """تحديث أوقات الصلاة يومياً لكل مستخدم بناءً على موقعه"""
    prefs = load_json(PREFS_FILE, {})
    for chat_id_str, data in prefs.items():
        if isinstance(data, dict) and 'lat' in data and 'lon' in data:
            try:
                lat = data['lat']
                lon = data['lon']
                url = "http://api.aladhan.com/v1/timings"
                params = {
                    "latitude": lat,
                    "longitude": lon,
                    "method": 2 # Islamic Society of North America (or any preferred method)
                }
                response = requests.get(url, params=params)
                res_data = response.json()
                
                if res_data["code"] == 200:
                    timings = res_data["data"]["timings"]
                    data['prayer_times'] = {
                        "Fajr": timings["Fajr"],
                        "Dhuhr": timings["Dhuhr"],
                        "Asr": timings["Asr"],
                        "Maghrib": timings["Maghrib"],
                        "Isha": timings["Isha"]
                    }
            except Exception as e:
                print(f"فشل جلب أوقات الأذان لـ {chat_id_str}: {e}")
                
    save_json(prefs, PREFS_FILE)
    print("✅ تم تحديث أوقات الأذان لجميع المستخدمين الذين سجلوا موقعهم.")

def job_check_adhan_times():
    """يتم تشغيلها كل دقيقة للتحقق من تطابق وقت المستخدم المحلي مع وقت الصلاة"""
    prefs = load_json(PREFS_FILE, {})
    for chat_id_str, data in prefs.items():
        if isinstance(data, dict) and 'prayer_times' in data and 'timezone' in data:
            try:
                user_tz = pytz.timezone(data['timezone'])
                utc_now = datetime.datetime.now(pytz.utc)
                local_time = utc_now.astimezone(user_tz)
                current_hm = local_time.strftime("%H:%M") # "15:30"
                
                lang = data.get("lang", "ar")
                
                for prayer_name, p_time in data['prayer_times'].items():
                    if current_hm == p_time:
                        # حان وقت الأذان
                        send_adhan_alert(chat_id_str, prayer_name, lang)
            except Exception as e:
                print(f"Error checking adhan for {chat_id_str}: {e}")

def send_adhan_alert(chat_id, prayer_name, lang):
    """إرسال رسالة الأذان بناءً على الصلاة واللغة"""
    prayer_ar = {"Fajr":"الفجر", "Dhuhr":"الظهر", "Asr":"العصر", "Maghrib":"المغرب", "Isha":"العشاء"}.get(prayer_name, prayer_name)
    prayer_en = prayer_name
    prayer_ku = {"Fajr":"سپێدێ", "Dhuhr":"نیڤرۆ", "Asr":"ئێڤاری", "Maghrib":"مەغریب", "Isha":"عەیشا"}.get(prayer_name, prayer_name)
    
    msgs = {
        "ar": f"🕌 **حان الآن موعد أذان {prayer_ar}**\nحسب التوقيت المحلي لمدينتك.",
        "en": f"🕌 **It is now time for {prayer_en} Adhan**\nAccording to your local time.",
        "ku_badini": f"🕌 **ئەڤە دەمێ بانگێ {prayer_ku} یە**\nل دویڤ دەمێ باژێرێ تە.",
        "ku_sorani": f"🕌 **کاتی بانگی {prayer_ku}یە**\nبەپێی کاتی ناوچەکەت."
    }
    
    bot.send_message(chat_id, msgs.get(lang, msgs["ar"]))
    
    # Send audio if configured
    prefs = load_json(PREFS_FILE, {})
    voice_key = prefs.get(str(chat_id), {}).get("adhan_voice", "abdulbasit") # Default to abdulbasit
    audio_url = ADHAN_AUDIO_URLS.get(voice_key)
    
    if audio_url and audio_url != "URL_OR_FILE_ID_HERE":
        try:
            bot.send_audio(chat_id, audio_url, title=f"أذان - {ADHAN_VOICES[voice_key]['ar']}")
        except Exception as e:
            print(f"Failed to send adhan audio for {chat_id}: {e}")
    
    # Send morning/evening adhkar automatically for Fajr and Asr/Maghrib
    if prayer_name == "Fajr":
        bot.send_message(chat_id, MORNING_ATHKAR)
    elif prayer_name == "Asr":
        bot.send_message(chat_id, EVENING_ATHKAR)

def job_morning():
    """أذكار الصباح"""
    send_to_all_custom("morning", lambda l: MORNING_ATHKAR)

def job_evening():
    """أذكار المساء"""
    send_to_all_custom("evening", lambda l: EVENING_ATHKAR)

def setup_daily_schedule():
    """يتم تشغيلها كل منتصف ليل لتحديث أوقات الصلاة وجدولتها"""
    print("🔄 تحديث جدول اليوم...")
    schedule.clear('daily_tasks')
    
    # 1. تحديث أوقات الأذان والتاريخ الهجري
    cache_adhan_times_for_all_users()
    fetch_current_hijri_date()
    
    # 2. جلب وقت الفجر وجدولته (للمستخدمين بدون موقع)
    fajr_time = get_fajr_time()
    schedule.every().day.at(fajr_time).do(job_morning).tag('daily_tasks')
    
    # 2. جدولة أذكار المساء
    schedule.every().day.at("17:00").do(job_evening).tag('daily_tasks')
    
    print(f"📅 تم جدولة أذكار الصباح على {fajr_time} وأذكار المساء على 17:00.")

def schedule_jobs():
    """إعداد وتشغيل الوظائف المجدولة"""
    
    # الدورة ستعمل كل 10 دقائق دائماً، ولكنها مصممة لتعمل بتزامن مع الساعة (00، 10، 20...)
    # ستبدأ بشكل فوري وتستمر لتعمل بشكل دوري
    # عندما تصل الساعة إلى 12:00 ستكون الدقيقة 00 وتعمل بشكل طبيعي ومنتظم.
    # لضمان بدءها بالضبط في بداية كل 10 دقائق، سنستخدم آلية أخرى لكن الجدول البسيط يعمل جيداً إذا شغلناه باقتراب وقت مضاعفات الـ 10
    
    # إعداد المهام اليومية (فجر، مساء) لأول مرة
    setup_daily_schedule()
    
    # تحديث الأوقات يومياً عند منتصف الليل
    schedule.every().day.at("00:01").do(setup_daily_schedule)
    
    # جدولة الدورة كل 10 دقائق
    schedule.every(10).minutes.at(":00").do(job_cycle)
    
    # تشغيل الدورة مرة واحدة فوراً عند التشغيل
    try:
        fetch_current_hijri_date()
        cache_adhan_times_for_all_users()
        job_cycle()
    except:
        pass
    
    # فحص أوقات الأذان كل دقيقة
    schedule.every(1).minutes.at(":00").do(job_check_adhan_times)
    
    while True:
        schedule.run_pending()
        time.sleep(1)

# ----------------- أوامر البوت ----------------- #
@bot.message_handler(commands=['lang'])
def cmd_lang(message):
    bot.reply_to(message, "اختر لغتك / Choose your language / زمانێ خۆ هەلبژێرە:", reply_markup=get_language_markup())

@bot.message_handler(commands=['start'])
def start_bot(message):
    chat_id = message.chat.id
    name = message.from_user.first_name if message.chat.type == 'private' else message.chat.title
    
    add_subscriber(chat_id)
    lang = get_user_lang(chat_id)
    welcome_msg = UI_TEXTS[lang]["welcome"].replace("[{name}]", name)
    
    bot.reply_to(message, welcome_msg, reply_markup=get_main_menu(lang))
    
    # إرسال الذكر المخصص
    title = UI_TEXTS[lang]["remind_athkar"]
    bot.send_message(chat_id, f"{title}\n\n{SPECIFIC_ATHKAR}")

@bot.message_handler(commands=['stop'])
def stop_bot(message):
    chat_id = message.chat.id
    lang = get_user_lang(chat_id)
    if remove_subscriber(chat_id):
        bot.reply_to(message, UI_TEXTS[lang]["stopped"])
    else:
        bot.reply_to(message, UI_TEXTS[lang]["not_registered"])

@bot.message_handler(commands=['athkar'])
def manually_send_athkar(message):
    chat_id = message.chat.id
    lang = get_user_lang(chat_id)
    selected_athkar = random.sample(ATHKAR, min(6, len(ATHKAR)))
    thikr_text = "\n\n 🌿 ━━━ 🌿 ━━━ 🌿 \n\n".join(selected_athkar)
    bot.reply_to(message, f"{UI_TEXTS[lang]['here_athkar']}\n\n{thikr_text}")

@bot.message_handler(commands=['hadith'])
def manually_send_hadith(message):
    chat_id = message.chat.id
    lang = get_user_lang(chat_id)
    selected_hadith = random.choice(AUTHENTIC_HADITHS)
    text = get_hadith_for_lang(lang, selected_hadith)
    bot.send_message(message.chat.id, f"{UI_TEXTS[lang]['remind_hadith']}\n\n{text}")

@bot.message_handler(commands=['morning'])
def manually_send_morning_athkar(message):
    bot.reply_to(message, MORNING_ATHKAR)

@bot.message_handler(commands=['evening'])
def manually_send_evenly_athkar(message):
    bot.reply_to(message, EVENING_ATHKAR)

@bot.message_handler(content_types=['location'])
def handle_location(message):
    chat_id = message.chat.id
    lang = get_user_lang(chat_id)
    
    if message.location:
        lat = message.location.latitude
        lon = message.location.longitude
        set_user_location(chat_id, lat, lon)
        
        thanks_msgs = {
            "ar": "✅ تم حفظ موقعك بنجاح! سيتم إرسال الأذان في وقته بناءً على منطقتك.",
            "en": "✅ Location saved! Adhan will be sent on time according to your region.",
            "ku_badini": "✅ جهێ تە هاتە پاراستن! بانگ دێ د دەمێ خۆ دا هێتە هنارتن ل دویڤ باژێرێ تە.",
            "ku_sorani": "✅ شوێنەکەت پارێزرا! بانگ لە کاتی خۆیدا دەنێردرێت بۆت بەپێی شارەکەت."
        }
        bot.reply_to(message, thanks_msgs.get(lang, thanks_msgs["ar"]))

@bot.message_handler(func=lambda message: True)
def handle_menu_buttons(message):
    chat_id = message.chat.id
    lang = get_user_lang(chat_id)
    text = message.text
    btns = UI_TEXTS[lang]["btns"]
    
    # التحقق من نوع الزر المضغوط بناءً على لغة المستخدم الحالية
    if text in [UI_TEXTS[l]["btns"]["morning"] for l in UI_TEXTS]:
        bot.reply_to(message, MORNING_ATHKAR)
        
    elif text in [UI_TEXTS[l]["btns"]["evening"] for l in UI_TEXTS]:
        bot.reply_to(message, EVENING_ATHKAR)
        
    elif text in [UI_TEXTS[l]["btns"]["hadith"] for l in UI_TEXTS]:
        selected_hadith = random.choice(AUTHENTIC_HADITHS)
        hadith_text = get_hadith_for_lang(lang, selected_hadith)
        bot.send_message(chat_id, f"{UI_TEXTS[lang]['remind_hadith']}\n\n{hadith_text}")
        
    elif text in [UI_TEXTS[l]["btns"]["random"] for l in UI_TEXTS]:
        selected_athkar = random.sample(ATHKAR, min(6, len(ATHKAR)))
        thikr_text = "\n\n 🌿 ━━━ 🌿 ━━━ 🌿 \n\n".join(selected_athkar)
        bot.reply_to(message, f"{UI_TEXTS[lang]['here_athkar']}\n\n{thikr_text}")
        
    elif text in [UI_TEXTS[l]["btns"].get("voice", "🗣 اختيار صوت الأذان") for l in UI_TEXTS]:
        msg = {
            "ar": "اختر صوت المؤذن الذي تفضله:",
            "en": "Choose your preferred Adhan reciter:",
            "ku_badini": "دەنگێ بانگبێژێ خۆ هەلبژێرە:",
            "ku_sorani": "دەنگی بانگبێژی خۆت هەڵبژێرە:"
        }.get(lang, "اختر صوت المؤذن الذي تفضله:")
        bot.reply_to(message, msg, reply_markup=get_voice_markup(lang))
        
    elif text in [UI_TEXTS[l]["btns"]["lang"] for l in UI_TEXTS]:
        bot.reply_to(message, "اختر لغتك / Choose your language / زمانێ خۆ هەلبژێرە:", reply_markup=get_language_markup())
        
    elif text in [UI_TEXTS[l]["btns"]["duas"] for l in UI_TEXTS]:
        dua = random.choice(QURANIC_DUAS)
        bot.reply_to(message, f"🤲 دعاء قرآني:\n\n{dua}")
        
    elif text in [UI_TEXTS[l]["btns"]["virtues"] for l in UI_TEXTS]:
        virtue_obj = random.choice(VIRTUES_OF_ATHKAR)
        if lang == "ar":
            virtue_text = virtue_obj["ar"]
        else:
            virtue_text = f"{virtue_obj['ar']}\n\n---\n{virtue_obj.get(lang, virtue_obj['en'])}"
        bot.reply_to(message, virtue_text)

# ----------------- التشغيل الأساسي ----------------- #
if __name__ == '__main__':
    # إعداد قائمة الأوامر في واجهة البوت
    try:
        commands = [
            telebot.types.BotCommand("start", "تفعيل البوت والاشتراك في الأذكار"),
            telebot.types.BotCommand("stop", "إيقاف إرسال الأذكار"),
            telebot.types.BotCommand("athkar", "طلب 4 أذكار الآن"),
            telebot.types.BotCommand("hadith", "طلب حديث شريف الآن"),
            telebot.types.BotCommand("morning", "أذكار الصباح"),
            telebot.types.BotCommand("evening", "أذكار المساء")
        ]
        bot.set_my_commands(commands)
    except Exception as e:
        print(f"لم يتم إعداد قائمة الأوامر: {e}")

    print("✅ تم تشغيل البوت بنجاح للمجموعات والأفراد!")
    print("⏳ جاري تشغيل الدورة الزمنية (دورة 50 دقيقة) وجلب أوقات الصلاة...")
    
    # تشغيل مجدول المهام في الخلفية
    scheduler_thread = threading.Thread(target=schedule_jobs)
    scheduler_thread.daemon = True 
    scheduler_thread.start()
    
    try:
        # إبقاء البوت متصل ومستعد لالتقاط الأوامر
        bot.infinity_polling(timeout=10, long_polling_timeout=5)
    except Exception as e:
        print(f"❌ حدث خطأ في الاتصال: {e}")
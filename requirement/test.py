from langchain.chains.summarize import load_summarize_chain

from langchain_community.llms.ollama import Ollama

from langchain.schema import Document







small_paragraph = """Nepal, a landlocked country nestled in the heart of the Himalayas in South Asia, is renowned for its breathtaking landscapes, rich cultural heritage, and diverse ecosystems. With an area of 147,516 square kilometers, Nepal is bordered by China to the north and India to the south, east, and west. The country's geography is marked by three distinct regions: the Terai, the Hill, and the Mountain region, which includes eight of the world's ten tallest mountains, including Mount Everest, the highest peak on Earth. The capital city, Kathmandu, is a vibrant hub of cultural and historical significance, home to ancient temples, palaces, and monuments that date back centuries. Kathmandu Valley, a UNESCO World Heritage site, encapsulates the rich artistic and architectural legacy of the Newar people. Major attractions include the Swayambhunath Stupa (also known as the Monkey Temple), Pashupatinath Temple, and Durbar Square, which showcase a blend of Hindu and Buddhist traditions. Nepal's population is incredibly diverse, with over 120 ethnic groups and 123 spoken languages. The predominant religion is Hinduism, followed by Buddhism, which together shape the country's festivals, rituals, and daily life. Dashain, Tihar, and Losar are among the most widely celebrated festivals, reflecting Nepal's rich cultural mosaic. The country's natural beauty extends beyond its towering peaks to lush valleys, dense forests, and serene lakes. Chitwan National Park and Sagarmatha National Park are UNESCO World Heritage sites that offer glimpses of Nepal extraordinary wildlife, including the Bengal tiger, one-horned rhinoceros, and red panda. Nepal's rivers, originating from the Himalayan glaciers, provide opportunities for rafting and kayaking, while trekking routes like the Annapurna Circuit and Everest Base Camp trek attract adventurers from around the globe. Nepal economy is primarily agrarian, but tourism plays a crucial role, driven by the allure of its natural and cultural treasures. Despite challenges such as political instability and natural disasters, the resilience and hospitality of the Nepali people continue to inspire visitors. As Nepal strides towards modernization, it remains deeply connected to its ancient traditions and the majestic beauty of its landscapes, offering a unique and enriching experience to all who visit. 



# Records mention the Gopalas and Mahishapalas believed to have been the earliest rulers with their capital at Matatirtha, the south-west corner of the Kathmandu Valley. From the 7th or 8th Century B.C. the Kirantis are said to have ruled the valley. Their famous King Yalumber is even mentioned in the epic, ‘Mahabharat’. Around 300 A.D. the Lichhavis arrived from northern India and overthrew the Kirantis. One of the legacies of the Lichhavis is the Changu Narayan Temple near Bhaktapur, a UNESCO World Heritage Site (Culture), which dates back to the 5th Century. In the early 7th Century, Amshuvarma, the first Thakuri king took over the throne from his father-in-law who was a Lichhavi. He married off his daughter Bhrikuti to the famous Tibetan King Tsong Tsen Gampo thus establishing good relations with Tibet. The Lichhavis brought art and architecture to the valley but the golden age of creativity arrived in 1200 A.D with the Mallas.



# During their 550 year rule, the Mallas built numerous temples and splendid palaces with picturesque squares. It was also during their rule that society and the cities became well organized; religious festivals were introduced and literature, music and art were encouraged. After the death of Yaksha Malla, the valley was divided into three kingdoms: Kathmandu (Kantipur), Bhaktapur (Bhadgaon) and Patan (Lalitpur). Around this time, the Nepal as we know it today was divided into about 46 independent principalities. One among these was the kingdom of Gorkha with a Shah ruler. Much of Kathmandu Valley’s history around this time was recorded by Capuchin friars who lived in the valley on their way in and out of Tibet.



# An ambitious Gorkha King named Prithvi Narayan Shah embarked on a conquering mission that led to the defeat of all the kingdoms in the valley (including Kirtipur which was an independent state) by 1769. Instead of annexing the newly acquired states to his kingdom of Gorkha, Prithvi Narayan decided to move his capital to Kathmandu establishing the Shah dynasty which ruled unified Nepal from 1769 to 2008.



# The history of the Gorkha state goes back to 1559 when Dravya Shah established a kingdom in an area chiefly inhabited by Magars. During the 17th and early 18thcenturies, Gorkha continued a slow expansion, conquering various states while forging alliances with others. Prithvi Narayan dedicated himself at an early age to the conquest of the Kathmandu Valley. Recognizing the threat of the British Raj in India, he dismissed European missionaries from the country and for more than a century, Nepal remained in isolation.



# During the mid-19th Century Jung Bahadur Rana became Nepal’s first prime minister to wield absolute power relegating the Shah king to mere figureheads. He started a hereditary reign of the Rana Prime Ministers that lasted for 104 years. The Ranas were overthrown in a democracy movement of the early 1950s with support from the-then monarch of Nepal, King Tribhuvan. Soon after the overthrow of the Ranas, King Tribhuvan was reinstated as the Head of the State. In early 1959, Tribhuvan’s son King Mahendra issued a new constitution, and the first democratic elections for a national assembly were held. The Nepali Congress Party was victorious and their leader, Bishweshwar Prasad Koirala formed a government and served as prime minister. But by 1960, King Mahendra had changed his mind and dissolved Parliament, dismissing the first democratic government.



# After many years of struggle when the political parties were banned, they finally mustered enough courage to start a People’s Movement in 1990. Paving way for democracy, the then-King Birendra accepted constitutional reforms and established a multiparty parliament with King as the Head of State and an executive Prime Minister. In May 1991, Nepal held its first parliamentary elections. In February 1996, the Maoist parties declared People’s War against monarchy and the elected government.



# Then on 1st June 2001, a horrific tragedy wiped out the entire royal family including King Birendra and Queen Aishwarya with many of their closest relatives. With only King Birendra’s brother, Gyanendra and his family surviving, he was crowned the king. King Gyanendra abided by the elected government for some time and then dismissed the elected Parliament to wield absolute power. In April 2006, another People’s Movement was launched jointly by the democratic parties focusing most energy in Kathmandu which led to a 19-day curfew. Eventually, King Gyanendra relinquished his power and reinstated the Parliament. On November 21, 2006, Prime Minister Girija Prasad Koirala and Maoist chairman Prachanda signed the Comprehensive Peace Agreement (CPA) 2006, committing to democracy and peace for the progress of the country and people. A Constituent Assembly election was held on April 10, 2008. On May 28, 2008, the newly elected Constituent Assembly declared Nepal a Federal Democratic Republic, abolishing the 240 year-old monarchy. Nepal today has a President as Head of State and a Prime Minister heading the Government.



# The Constituent Assembly made significant progress to accomplish the mandate of writing a new democratic constitution of Nepal during its first 4 years term. The country also had an extensive democratic exercise in that direction including collection of public inputs on the contents of the new constitution and intense deliberations in the Assembly. However, due to political disagreements on some of the contentious issues like federal provinces and form of government, the first CA could not accomplish the historic task and there was natural termination of its mandate in 2012. The election of CA II was held in November 2013 and in its first meeting, leaders of political parties set the timeline of 1 year to complete the task of writing the new constitution.



# Devastating earthquake of 7.8 magnitude hit Nepal in April 2015 followed by several powerful aftershocks causing loss of life, infrastructure and property in an unimaginable scale. Most mid hill districts of Nepal including Kathmandu valley saw massive devastation. This terrible experience created a sense of urgency among political parties to expedite the constitution writing so that a political process would come to a meaningful conclusion and country can divert all its focus on post disaster reconstruction.



# After weeks of zeroing in on most contentious issues, political parties sorted them out paving the way to finalize the constitution. The new constitution of Nepal was promulgated through an overwhelming majority of the votes of CA members on September 20, 2015. With this historic achievement, the decades-long dream of Nepali people to have a constitution made through an elected representative body has now been realized. As per the provisions of the new constitution, elections of the new President, Prime Ministers and some other State positions have been successfully held.

# """ 



# small_paragraph = """ The sun rises high,\\nA bright new day in the sky."""





import pandas as pd # Adjust these imports to your actual modules


from requests.exceptions import RequestException

# Sample definition of the function



# Convert the 'test' dictionary to a DataFrame

# samsum_chain_test_df = pd.DataFrame(samsum['test'])



# samsum_chain_test_df = samsum_chain_test_df[:10]



# Apply the function to the 'dialogue' column to convert to Document objects



# Load the language model

llm = Ollama(model="qwen2:0.5b")





def invoke(document):

    paragraph_docs = Document(page_content= document)



    docs = [paragraph_docs]

    chain_refine = load_summarize_chain(llm, chain_type = "stuff")



    result_refine = chain_refine.invoke(docs)



    try:

        result_refine = chain_refine.invoke(docs)

        return result_refine['output_text']

    except RequestException as e:

        # Log the error or handle it as necessary

        return f"An error occurred: {str(e)}"

   



# Apply `invoke` function to each row in the DataFrame

# samsum_chain_test_df['summary_generated'] = samsum_chain_test_df['dialogue'].apply(invoke)

result = invoke(small_paragraph)

print(result)
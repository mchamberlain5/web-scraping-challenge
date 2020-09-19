#dependencies
from splinter import Browser
from bs4 import BeautifulSoup as bs
import time
# Choose the executable path to driver 
executable_path = {'executable_path': 'chromedriver.exe'}
browser = Browser('chrome', **executable_path, headless=False)
def scrape():
	news_title,news_p = news_scrape()
	featured_image_url = img_scrape()
	mars_df = fact_scrape()
	mars_hemi = hemispheres_scrape()
	scrape_dict = {
		'news title':news_title,
		'news paragraph': news_p,
		'featured image': featured_image_url,
		'mars facts': mars_df,
		'mars hemisphere': mars_hemi
	}
	print(scrape_dict)

def news_scrape():
# Visit Nasa news url through splinter module
	url = 'https://mars.nasa.gov/news/'
	browser.visit(url)
# HTML Object
	html = browser.html
# Parse HTML with Beautiful Soup
	soup = bs(html, 'html.parser')
# Retrieve the latest element that contains news title and news_paragraph
	news_text = soup.find('div', class_='list_text')
	news_title = news_text.find('div', class_='content_title').text
	news_p = soup.find('div', class_='article_teaser_body').text
	return news_title,news_p

def img_scrape():
	image_url_featured = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
	browser.visit(image_url_featured)
	# HTML Object 
	html_image = browser.html
	# Parse HTML with Beautiful Soup
	soup = bs(html_image, 'html.parser')
	# Retrieve background-image url from style tag 
	featured_image_url  = soup.find('article')['style'].replace('background-image: url(','').replace(');', '')[1:-1]
	# Website Url 
	main_url = 'https://www.jpl.nasa.gov'
	# Concatenate website url with scrapped route
	featured_image_url = main_url + featured_image_url
	# Display full link to featured image
	return featured_image_url
def fact_scrape():
	# Visit Mars facts url 
	facts_url = 'http://space-facts.com/mars/'
	# Use Panda's `read_html` to parse the url
	mars_facts = pd.read_html(facts_url)
	# Find the mars facts DataFrame in the list of DataFrames as assign it to `mars_df`
	mars_df = mars_facts[0]
	# Assign the columns `['Description', 'Value']`
	mars_df.columns = ['Description','Value']
	# Set the index to the `Description` column without row indexing
	mars_df.set_index('Description', inplace=True)
	# Save html code to folder Assets
	mars_df.to_html()
	data = mars_df.to_dict(orient='records')  
	# Display mars_df
	return mars_df

def hemispheres_scrape():
		#visit mars hemispheres url
	hemisphere_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
	browser.visit(hemisphere_url)

	#create html object
	hemisphere_html = browser.html

	#use bs to parse through html object
	soup= bs(hemisphere_html, 'html.parser')

	#find all items on page
	hemi_items = soup.find_all('div', class_='item')

	#create image url list to append to 
	img_url_list =[]

	#save base url
	base_url = 'https://astrogeology.usgs.gov/'

	#create loop to add items to list
	for i in hemi_items: 
	    # Store title
	    title = i.find('h3').text
	    
	    # Store link that leads to full image website
	    partial_img_url = i.find('a', class_='itemLink product-item')['href']
	    
	    # Visit the link that contains the full image website 
	    browser.visit(base_url + partial_img_url)
	    
	    # HTML Object of individual hemisphere information website 
	    partial_img_html = browser.html
	    
	    # Parse HTML with Beautiful Soup for every individual hemisphere information website 
	    soup = bs(partial_img_html, 'html.parser')
	    
	    # Retrieve full image source 
	    img_url = base_url + soup.find('img', class_='wide-image')['src']
	    
	    # Append the retreived information into a list of dictionaries 
	    img_url_list.append({"title" : title, "img_url" : img_url})
	    

	# Display hemisphere_image_urls
	return img_url_list

if __name__ == "__main__":
	scrape()
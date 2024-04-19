"""This script serves as an example on how to use Python 
   & Playwright to scrape/extract data from Google Maps"""

from playwright.sync_api import sync_playwright
from dataclasses import dataclass, asdict, field
import pandas as pd
import argparse
import os
import sys

@dataclass
class Business:
    """holds business data"""

    name: str = None
    address: str = None
    website: str = None
    phone_number: str = None
    reviews_count: int = None
    reviews_average: float = None
    latitude: float = None
    longitude: float = None


@dataclass
class BusinessList:
    """holds list of Business objects,
    and save to both excel and csv
    """
    business_list: list[Business] = field(default_factory=list)
    save_at = 'output'

    def dataframe(self):
        """transform business_list to pandas dataframe

        Returns: pandas dataframe
        """
        return pd.json_normalize(
            (asdict(business) for business in self.business_list), sep="_"
        )

    def save_to_excel(self, filename):
        """saves pandas dataframe to excel (xlsx) file

        Args:
            filename (str): filename
        """

        if not os.path.exists(self.save_at):
            os.makedirs(self.save_at)
        try:
            self.dataframe().to_excel(f"output/{filename}.xlsx", index=False) #nanu cambio
            print("Bien a la 1")

        except:
            try:
                self.dataframe().to_excel(f"output\{filename}.xlsx", index=False)
                print("Bien a la 2")
            except:
                try:
                    self.dataframe().to_excel(f"{filename}.xlsx", index=False)
                    print("Bien a la 3")
                except:
                    print("todo mal")
                    

    def save_to_csv(self, filename):
        """saves pandas dataframe to csv file

        Args:
            filename (str): filename
        """

        if not os.path.exists(self.save_at):
            os.makedirs(self.save_at)
        self.dataframe().to_csv(f"output/{filename}.csv", index=False)

def extract_coordinates_from_url(url: str) -> tuple[float,float]:
    """helper function to extract coordinates from url"""
    
    coordinates = url.split('/@')[-1].split('/')[0]
    # return latitude, longitude
    return float(coordinates.split(',')[0]), float(coordinates.split(',')[1])

def main():
    
    ########
    # input 
    ########
    
    # read search from arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--search", type=str)
    parser.add_argument("-t", "--total", type=int)
    args = parser.parse_args()
    
    if args.search:
        search_list = [args.search]
    
    if args.total:
        total = args.total
    else:
        # if no total is passed, we set the value to random big number
        total = 1_000_000

    if not args.search:
        search_list = []
        # read search from input.txt file
        input_file_name = 'input.txt'
        # Get the absolute path of the file in the current working directory
        input_file_path = os.path.join(os.getcwd(), input_file_name)
        # Check if the file exists
        if os.path.exists(input_file_path):
        # Open the file in read mode
            with open(input_file_path, 'r') as file:
            # Read all lines into a list
                search_list = file.readlines()
        #modificado por nanu
        search_list = [elemento.rstrip('\n') for elemento in search_list]

        print(search_list)

        #termina modificado por nanu        
                
        if len(search_list) == 0:
            print('Error occured: You must either pass the -s search argument, or add searches to input.txt')
            sys.exit()
        
    ###########
    # scraping
    ###########
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        #modificado nanu
        # lo que habia antes= page.goto("https://www.google.com/maps", timeout=60000) 
        page.goto("https://www.google.com/maps/search/hotel/@-49.3091202,-67.7351463,15z?entry=ttu", timeout=60000)
        #Se deben poner los enlaces con el posicionamiento de las ciudades
        enlaces = [
            "https://www.google.com/maps/search/hotel/@-49.3091202,-67.7351463,15z?entry=ttu",
            "https://www.google.com/maps/search/hotel/@-54.5318911,-67.2032165,14z/data=!4m2!2m1!6e3?entry=ttu"]
        #termina la modificacion nanu

        # wait is added for dev phase. can remove it in production
        page.wait_for_timeout(2000)
        #modificado nanu
        business_list = BusinessList()
        #termina modificado nanu

        for search_for_index, search_for in enumerate(search_list):
            print(f"-----\n{search_for_index} - {search_for}".strip())
            #modificado nanu
            #en cada iteracion se cambia de ciudad en la lista
            page.goto(enlaces[search_for_index], timeout=60000)
            #termina la modificacion nanu
            page.locator('//input[@id="searchboxinput"]').fill(search_for)
            page.wait_for_timeout(2000)

            page.keyboard.press("Enter")
            page.wait_for_timeout(2000)

            # scrolling
            page.hover('//a[contains(@href, "https://www.google.com/maps/place")]')

            # this variable is used to detect if the bot
            # scraped the same number of listings in the previous iteration
            previously_counted = 0
            while True:
                page.mouse.wheel(0, 10000)
                page.wait_for_timeout(1000)

                if (
                    page.locator(
                        '//a[contains(@href, "https://www.google.com/maps/place")]'
                    ).count()
                    >= total
                ):
                    listings = page.locator(
                        '//a[contains(@href, "https://www.google.com/maps/place")]'
                    ).all()[:total]
                    listings = [listing.locator("xpath=..") for listing in listings]
                    print(f"Total Scraped: {len(listings)}")
                    break
                else:
                    # logic to break from loop to not run infinitely
                    # in case arrived at all available listings
                    if (
                        page.locator(
                            '//a[contains(@href, "https://www.google.com/maps/place")]'
                        ).count()
                        == previously_counted
                    ):
                        listings = page.locator(
                            '//a[contains(@href, "https://www.google.com/maps/place")]'
                        ).all()
                        print(f"Arrived at all available\nTotal Scraped: {len(listings)}")
                        break
                    else:
                        previously_counted = page.locator(
                            '//a[contains(@href, "https://www.google.com/maps/place")]'
                        ).count()
                        print(
                            f"Currently Scraped: ",
                            page.locator(
                                '//a[contains(@href, "https://www.google.com/maps/place")]'
                            ).count(),
                        )

            #business_list = BusinessList() modificado nanu

            # scraping
            for listing in listings:
                try:
                    listing.click()
                    page.wait_for_timeout(1000)

                    name_attibute = 'aria-label'
                    address_xpath = '//button[@data-item-id="address"]//div[contains(@class, "fontBodyMedium")]'
                    website_xpath = '//a[@data-item-id="authority"]//div[contains(@class, "fontBodyMedium")]'
                    phone_number_xpath = '//button[contains(@data-item-id, "phone:tel:")]//div[contains(@class, "fontBodyMedium")]'
                    review_count_xpath = '//button[@jsaction="pane.reviewChart.moreReviews"]//span'
                    reviews_average_xpath = '//div[@jsaction="pane.reviewChart.moreReviews"]//div[@role="img"]'
                    
                    
                    business = Business()
                   
                    if len(listing.get_attribute(name_attibute)) >= 1:
        
                        business.name = listing.get_attribute(name_attibute)
                    else:
                        business.name = ""
                    if page.locator(address_xpath).count() > 0:
                        business.address = page.locator(address_xpath).all()[0].inner_text()
                    else:
                        business.address = ""
                    if page.locator(website_xpath).count() > 0:
                        business.website = page.locator(website_xpath).all()[0].inner_text()
                    else:
                        business.website = ""
                    if page.locator(phone_number_xpath).count() > 0:
                        business.phone_number = page.locator(phone_number_xpath).all()[0].inner_text()
                        #editado nanu
                        #se formatea el numero 
                        business.phone_number = business.phone_number.replace(' ','')
                        business.phone_number = business.phone_number.replace('-','')
                        if(business.phone_number[0]=='0'):
                            business.phone_number= business.phone_number[1:]
                        #termina editado nanu
                    else:
                        business.phone_number = ""
                    if page.locator(review_count_xpath).count() > 0:
                        business.reviews_count = int(
                            page.locator(review_count_xpath).inner_text()
                            .split()[0]
                            .replace(',','')
                            .strip()
                        )
                    else:
                        business.reviews_count = ""
                        
                    if page.locator(reviews_average_xpath).count() > 0:
                        business.reviews_average = float(
                            page.locator(reviews_average_xpath).get_attribute(name_attibute)
                            .split()[0]
                            .replace(',','.')
                            .strip())
                    else:
                        business.reviews_average = ""
                    
                    
                    business.latitude, business.longitude = extract_coordinates_from_url(page.url)

                    business_list.business_list.append(business)
                except Exception as e:
                    print(f'Error occured: {e}')
            
            #########
            # output
            #########
        business_list.save_to_excel(f"google_maps_data_{search_for}_{search_for_index}".replace(' ', '_'))
        business_list.save_to_csv(f"google_maps_data_{search_for}_{search_for_index}".replace(' ', '_'))

        browser.close()


if __name__ == "__main__":
    main()

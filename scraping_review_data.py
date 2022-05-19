import pandas as pd
import re
from datetime import date, timedelta

def review_data_collection(soup):
    '''
    Extract review data from dslreports.com 
    Arguments: soup: a BeautifulSoup object that represents a single DSL Reports web page that 
    contains ISP reviews.
    Returns: a Pandas DataFrame that contains review data using the following columns:
        ['review_by', 'review_id', 'days_or_years_since_review', 'location', 'cost', 
        'installation_time', 'provider', 'pre_sales_information', 'install_co-ordination', 
        'connection_reliability', 'tech_support', 'services', 'value_for_money']
    '''
    
    # Find all reviews in a single web page:
    try:
        reviews_list = soup.find_all('a', {'name':re.compile('review\d')})
        if reviews_list == []:
            print('No reviews in this page. End.')
            return
    except IndexError as ie:
        print(ie)
        return
        
    reviews_list = [review.parent for review  in reviews_list]


    # We initialize the list review_data_list that will hold dictionaries that contain the 
    # different attributes of each review
    review_data_list = []

    #print('Rows', end = '\t')
    i=0
    for review in reviews_list:
        # initialize a dict that will hold the data of each row (review)
        review_data = dict()
        i+=1
        #print(i, end = '\t')

        # Find when a review was posted or updated
        # Remove from the soup the content of the div tag that include the information about other reviews 
        # by the same reviewer. (they use the class 'soft-tbl-10'). This is only present is some reviews.
        try:
            review.find('div', class_ = 'soft-tbl-10').extract()
        except AttributeError:
            pass
        
        # Some reviews have attached pictures within a div tag
        # Attachments: <div class="news_tiny_center"> <!-- tiny_attach --> ....
        # This should also be removed from the soup.
        try:
            for attach_tag in review.find_all(text=re.compile('tiny_attach')):
                  attach_tag.parent.extract()
        except AttributeError:
            pass       

        # After the soup clean-up above, the required 'age' of a review will always be included 
        # within the 2nd div tag.
        try:
            review_date_string = review.find_all('div')[1].find(string = re.compile('(updated)|(lodged)'))
            review_data['days_or_years_since_review'] = ' '.join(review_date_string.split(' ')[1:3])
        except AttributeError:
            pass


        # The first table within each review includes all the required data aside from the posting date.
        # The table has one row and two cells.
        review_table = review.find('table')

        # Scrap the review data included in the first cell
        first_cell = review_table.find_all('td')[0]
        
        try:
            rev_by = first_cell.find('div').text.split(' ')
            if rev_by[0].lower() + '_' + rev_by[1] == 'review_by':
                review_data['review_by'] = ' '. join(rev_by[2:])
            else:
                pass
        except AttributeError:
            pass

        try:
            review_data['review_id'] = first_cell.find_all('a')[1]['name']
        except:
            pass

        for item in first_cell.find_all('li'):
            item = item.text.split(' ')
            key = item[0].strip(':').lower()  
            if key == 'location':
                review_data[key] = ' '.join(item[1:])
            elif key == 'cost':
                val = item[1].strip('$')
                if val.isdigit():
                    review_data[key] = val
            elif key == 'install':
                review_data['installation_time'] = re.findall('^\D*(\d+)\D*', ' '.join(item[1:]))[0]

        try:
            review_data['provider'] = review_table.find_all('td')[0] \
                                                  .find('img', {'alt': 'Telco party'}) \
                                                  .find_next_sibling('b') \
                                                  .text
        except AttributeError:
            pass


        # Scrap the review data included in the 2nd cell
        # The ratings are included in the name of images. See this example:
        # <b>Install Co-ordination</b>:<IMG WIDTH=70 HEIGHT=10 ALIGN=ABSMIDDLE SRC="//i.dslr.net/bars/50_sm.gif">
        
        second_cell = review_table.find_all('td')[1]
        for (key, value)  in zip(second_cell.find_all('b'), second_cell.find_all('img')):
            key = key.text
            key = '_'.join(key.split(' ')).lower()
            review_data[key]  = re.findall('\D*(\d*)', value['src'])[0]


        # Finally we append the data of each row to the list
        review_data_list.append(review_data)
     
    #return a dataframe using the list above and return it.
    
    col = ['review_by', 'review_id', 'days_or_years_since_review', 'location', \
            'cost', 'installation_time', 'provider', 'pre_sales_information', \
            'install_co-ordination', 'connection_reliability', 'tech_support', 'services', 'value_for_money']
    
    return pd.DataFrame(review_data_list, columns = col)


def find_date(elapsed_time):
    ''' 
    Get the review date from the elapsed time
    Arguments: elapsed_time (string) with the format 'x day(s)' or 'x year(s)' where x is the number of 
    days/years since a review was posted or last updated.
    Returns: date when the review was posted or last updated.
    '''
    
    num_years_or_days = str(elapsed_time).split(' ')
    # We want to match both year(day) and years(days)
    if 'year' in num_years_or_days[-1]:  
        review_date = date.today() - timedelta(days=float(num_years_or_days[0]) * 365.25)
        return review_date.isoformat()
    elif 'day' in num_years_or_days[-1]:
        review_date = date.today() - timedelta(days=float(num_years_or_days[0]))
        return review_date.isoformat()
    #else:
        # raise Exception('Check the elapsted time. This function expects the format x day(s) or x year(s) \
        # where x is the number of days/years since a review was posted or last updated.')

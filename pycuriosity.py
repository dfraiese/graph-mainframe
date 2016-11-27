#!/usr/bin/env python
# -*- coding: utf-8
#!/usr/bin/python

from BeautifulSoup import BeautifulSoup
import urllib2
import urllib
from PIL import Image, ImageDraw, ImageFont
import os
from decimal import Decimal
import imageio
import datetime
import sys

CAMERA01 = 'FLA_'
CAMERA02 = 'FLB_'
PATH = '/home/diego/MSL2/'

n_cant_images = 0
l_images = []

if __name__ == "__main__":
    try:
        SOLSTART = int(sys.argv[1])
        PATH = sys.argv[2]
    except Exception, e:
        print 'ERROR ', e

    s_now = str(datetime.datetime.now())
    
    html_page = urllib2.urlopen('http://curiosityrover.com/tracking/drivelog.html')
    soup = BeautifulSoup(html_page)

    d_sol = {}
    
    l_sols = []
    
    n_odometer = 0
    
    for i in soup.findAll(attrs={'class' : 'evenitem'}):
        html_dist = i.contents[1]
        html_sol = i.contents[3]
        html_date = i.contents[4]
        
        s_sol = html_sol.text[:html_sol.text.find(' ')]
        
        l_sols.append(int(s_sol))
        
        n_dist = Decimal(html_dist.text)
        
        d_date = html_date.text[:html_date.text.find(' ')]
        
        l_sol_data = []
        d_sol.setdefault(s_sol, l_sol_data)
        l_sol_data.append(n_dist)
        l_sol_data.append(d_date)
        
    for i in soup.findAll(attrs={'class' : 'odditem'}):
        html_dist = i.contents[1]
        html_sol = i.contents[3]
        html_date = i.contents[4]
        
        s_sol = html_sol.text[:html_sol.text.find(' ')]
        
        l_sols.append(int(s_sol))
        
        n_dist = Decimal(html_dist.text)
        
        d_date = html_date.text[:html_date.text.find(' ')]
        
        l_sol_data = []
        d_sol.setdefault(s_sol, l_sol_data)
        l_sol_data.append(n_dist)
        l_sol_data.append(d_date)
        
    SOLEND = max(l_sols)
    #SOLEND = 17
    
    print 'ARGS ', SOLSTART, SOLEND, PATH

    l_sols.sort()
    
    d_odometer = {}
    n_odometer_tot = 0
    
    for i in l_sols:
        n_odometer_tot = n_odometer_tot + d_sol[str(i)][0]
        d_odometer.setdefault(i, n_odometer_tot)
    
    for i in range(SOLSTART, SOLEND + 1):
        print 'SOL=' + str(i)
        
        html_page = urllib2.urlopen('http://mars.nasa.gov/msl/multimedia/raw/?s=' + str(i) + '&camera=FHAZ_')
        soup = BeautifulSoup(html_page)
    
        tmp_date = ''
        tmp_dist = ''
        tmp_odometer = ''
        
        for j in d_sol:
            if str(i) == str(j):
                tmp_dist = str(d_sol[j][0])
                tmp_date = str(d_sol[j][1])
                            
                n_odometer = d_odometer[int(j)]
                            
                tmp_odometer = str(n_odometer)
                break
                
        for link in soup.findAll('a'):
            s_link = link.get('href')
        
            if (s_link != None) and ('fcam/' + CAMERA01 in s_link) and ('.JPG' in s_link):
                start = s_link.find(CAMERA01) 
                image = urllib.URLopener()
                
                name_image = 'SOL' + str(i) + '-' + s_link[start:]
                
                f = image.open(s_link)
                im = Image.open(f)
                
                if im.size == (1024, 1024):
                    print name_image + ' ' + str(im.size), ' odometer', n_odometer
            
                    draw = ImageDraw.Draw(im)
            
                    font = ImageFont.truetype('/usr/share/fonts/truetype/ubuntu-font-family/TlwgTypewriter.ttf', 25)
                    draw.text((0, 0), 'SOL ' + str(i) + ' ODOMETER ' + str(n_odometer), font=font, fill='white')
                    
                    if tmp_date != '':
                        draw.text((0, 25), 'DATE ' + tmp_date + ' DISTANCE ' + tmp_dist, font=font, fill='white')
                        
                    font = ImageFont.truetype('/usr/share/fonts/truetype/ubuntu-font-family/TlwgTypewriter.ttf', 20)
                    draw.text((0, 950), 'CURIOSITY ROVER', font=font, fill='white')
                    draw.text((0, 970), 'FRONT LEFT CAM', font=font, fill='white')
                    draw.text((0, 990), 'NASA / JPL', font=font, fill='white')
                    draw.text((840, 990), '//Diego Fraiese', font=font, fill='white')
                    
                    im.save(PATH + name_image)
                    
                    n_cant_images = n_cant_images + 1
                    l_images.append(name_image)

        for link in soup.findAll('a'):
            s_link = link.get('href')
        
            if (s_link != None) and ('fcam/' + CAMERA02 in s_link) and ('.JPG' in s_link):
                start = s_link.find(CAMERA02) 
                image = urllib.URLopener()
                
                name_image = 'SOL' + str(i) + '-' + s_link[start:]
                
                f = image.open(s_link)
                im = Image.open(f)
                
                if im.size == (1024, 1024):
                    print name_image + ' ' + str(im.size), ' odometer', n_odometer
            
                    draw = ImageDraw.Draw(im)
            
                    font = ImageFont.truetype('/usr/share/fonts/truetype/ubuntu-font-family/TlwgTypewriter.ttf', 25)
                    draw.text((0, 0), 'SOL ' + str(i) + ' ODOMETER ' + str(n_odometer), font=font, fill='white')
                    
                    if tmp_date != '':
                        draw.text((0, 25), 'DATE ' + tmp_date + ' DISTANCE ' + tmp_dist, font=font, fill='white')
                        
                    font = ImageFont.truetype('/usr/share/fonts/truetype/ubuntu-font-family/TlwgTypewriter.ttf', 20)
                    draw.text((0, 950), 'CURIOSITY ROVER', font=font, fill='white')
                    draw.text((0, 970), 'FRONT LEFT CAM', font=font, fill='white')
                    draw.text((0, 990), 'NASA / JPL', font=font, fill='white')
                    draw.text((840, 990), '//Diego Fraiese', font=font, fill='white')
                    
                    im.save(PATH + name_image)

                    n_cant_images = n_cant_images + 1
                    l_images.append(name_image)

    print 'BUILDING HTML'
    
    f = open(PATH + 'index2.html', 'w')
    
    s_html01 = """
<html>
<head>
<meta http-equiv="content-type" content="text/html; charset=UTF-8"> 
<script src="https://ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js"></script>
<link href='https://fonts.googleapis.com/css?family=Lobster' rel='stylesheet' type='text/css'>
<link rel="stylesheet" href="jquery.imageplayer.css">
<script src="jquery.imageplayer.js"></script>

<script>
  var _gaq = _gaq || [];
  _gaq.push(['_setAccount', 'UA-30057581-1']);
  _gaq.push(['_trackPageview']);

  (function() {
    var ga = document.createElement('script'); ga.type = 'text/javascript'; ga.async = true;
    ga.src = ('https:' == document.location.protocol ? 'https://ssl' : 'http://www') + '.google-analytics.com/ga.js';
    var s = document.getElementsByTagName('script')[0]; s.parentNode.insertBefore(ga, s);
  })();
</script>
</head>

<body>
   <section>
      <style type="text/css">
              p {color: Grey; 
                font-family: courier; 
                text-align: center; 
                display: block;
                margin-top: 0;
                margin-bottom: 0;
                margin-left: 0:
                margin-right: 0;
                font-size:30px;}
              footer {color: Grey; 
                font-family: courier; 
                text-align: center; 
                display: block;
                margin-top: 0;
                margin-bottom: 0;
                margin-left: 0:
                margin-right: 0;
                font-size:15px;}

              div {margin: 10 auto; width: 1064px;}
      </style>
      <div>
         <p>MSL CURIOSTY</p>
    """    
    
    s_html02 = '<p>Last update ' + s_now[0:10] + ' - ' + str(n_cant_images) + ' pictures processed</p>'
    
    s_html03 = """
    </div>
    </section>
    <div>
    <ul id="image_player">
    """
    
    f.write(s_html01 + '\n')
    f.write(s_html02 + '\n')
    f.write(s_html03 + '\n')
    
    for i in l_images:
        s_tmp = '<li><img src="./' + i + '" /></li>'
        f.write(s_tmp + '\n')

    s_html04 = """
    </ul>

    <script>
          $(function() {
              var options = {
                  stageWidth:1064,
                  stageHeight:680,
                  autoStart:false,
                  pauseOnHover:true,
                  delay:1,
                  loop:true
           };
           $('#image_player').imagePlayer(options);
           });
     </script>
     </div>
     <footer>Images from NASA / JPL - Tracks from curiosityrover.com</footer>
     <footer>(C) November 2016 - Diego Fraiese - dfraiese@gmail.com</footer>
</body>
</html>    
    """
    
    f.write(s_html04 + '\n')
    print "END"


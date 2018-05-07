#ip location
#
#Requirements:
#pip install python-geoip-geolite2
#pip install python-geoip

import requests
from geoip import geolite2

#dict for converting country codes to country name
country_codes = {'BD': 'Bangladesh', 'BE': 'Belgium', 'BF': 'Burkina Faso', 'BG': 'Bulgaria', 
'BA': 'Bosnia and Herzegovina', 'BB': 'Barbados', 'WF': 'Wallis and Futuna', 'BM': 'Bermuda', 
'BN': 'Brunei Darussalam', 'BO': 'Bolivia', 'BH': 'Bahrain', 'BI': 'Burundi', 'BJ': 'Benin', 
'BT': 'Bhutan', 'JM': 'Jamaica', 'BV': 'Bouvet Island', 'BW': 'Botswana', 'WS': 'Samoa', 
'BR': 'Brazil', 'BS': 'Bahamas', 'JE': 'Jersey', 'BY': 'Belarus', 'BZ': 'Belize', 
'RU': 'Russian Federation', 'RW': 'Rwanda', 'RS': 'Serbia', 'TL': 'Timor-leste', 'RE': 'Reunion', 
'TM': 'Turkmenistan', 'TJ': 'Tajikistan', 'RO': 'Romania', 'TK': 'Tokelau', 'GW': 'Guinea-bissau', 
'GU': 'Guam', 'GT': 'Guatemala', 'GS': 'South Georgia and The South Sandwich Islands', 'GR': 'Greece', 
'GQ': 'Equatorial Guinea', 'GP': 'Guadeloupe', 'JP': 'Japan', 'GY': 'Guyana', 'GG': 'Guernsey', 
'GF': 'French Guiana', 'GE': 'Georgia', 'GD': 'Grenada', 'GB': 'United Kingdom', 'GA': 'Gabon', 
'GN': 'Guinea', 'GM': 'Gambia', 'GL': 'Greenland', 'GI': 'Gibraltar', 'GH': 'Ghana', 'OM': 'Oman', 
'TN': 'Tunisia', 'JO': 'Jordan', 'HR': 'Croatia', 'HT': 'Haiti', 'HU': 'Hungary', 'HK': 'Hong Kong', 
'HN': 'Honduras', 'HM': 'Heard Island and Mcdonald Islands', 'VE': 'Venezuela', 'PR': 'Puerto Rico', 
'PS': 'Palestinian Territory, Occupied', 'PW': 'Palau', 'PT': 'Portugal', 'KN': 'Saint Kitts and Nevis', 
'PY': 'Paraguay', 'IQ': 'Iraq', 'PA': 'Panama', 'PF': 'French Polynesia', 'PG': 'Papua New Guinea', 
'PE': 'Peru', 'PK': 'Pakistan', 'PH': 'Philippines', 'PN': 'Pitcairn', 'PL': 'Poland', 
'PM': 'Saint Pierre and Miquelon', 'ZM': 'Zambia', 'EH': 'Western Sahara', 'EE': 'Estonia', 'EG': 'Egypt', 
'ZA': 'South Africa', 'EC': 'Ecuador', 'IT': 'Italy', 'VN': 'Viet Nam', 'SB': 'Solomon Islands', 'ET': 'Ethiopia', 
'SO': 'Somalia', 'ZW': 'Zimbabwe', 'SA': 'Saudi Arabia', 'ES': 'Spain', 'ER': 'Eritrea', 'ME': 'Montenegro', 
'MD': 'Moldova, Republic of', 'MG': 'Madagascar', 'MA': 'Morocco', 'MC': 'Monaco', 'UZ': 'Uzbekistan', 
'MM': 'Myanmar', 'ML': 'Mali', 'MO': 'Macao', 'MN': 'Mongolia', 'MH': 'Marshall Islands', 
'MK': 'Macedonia, The Former Yugoslav Republic of', 'MU': 'Mauritius', 'MT': 'Malta', 'MW': 'Malawi', 'MV': 'Maldives', 
'MQ': 'Martinique', 'MP': 'Northern Mariana Islands', 'MS': 'Montserrat', 'MR': 'Mauritania', 'IM': 'Isle of Man', 
'UG': 'Uganda', 'TZ': 'Tanzania, United Republic of', 'MY': 'Malaysia', 'MX': 'Mexico', 'IL': 'Israel', 
'FR': 'France', 'AW': 'Aruba', 'SH': 'Saint Helena', 'SJ': 'Svalbard and Jan Mayen', 'FI': 'Finland', 'FJ': 'Fiji', 
'FK': 'Falkland Islands (Malvinas)', 'FM': 'Micronesia, Federated States of', 'FO': 'Faroe Islands', 
'NI': 'Nicaragua', 'NL': 'Netherlands', 'NO': 'Norway', 'NA': 'Namibia', 'VU': 'Vanuatu', 'NC': 'New Caledonia', 
'NE': 'Niger', 'NF': 'Norfolk Island', 'NG': 'Nigeria', 'NZ': 'New Zealand', 'NP': 'Nepal', 'NR': 'Nauru', 
'NU': 'Niue', 'CK': 'Cook Islands', 'CI': "Cote D'ivoire", 'CH': 'Switzerland', 'CO': 'Colombia', 'CN': 'China', 
'CM': 'Cameroon', 'CL': 'Chile', 'CC': 'Cocos (Keeling) Islands', 'CA': 'Canada', 'CG': 'Congo', 
'CF': 'Central African Republic', 'CD': 'Congo, The Democratic Republic of The', 'CZ': 'Czechia', 'CY': 'Cyprus', 
'CX': 'Christmas Island', 'CR': 'Costa Rica', 'CV': 'Cape Verde', 'CU': 'Cuba', 'SZ': 'Swaziland', 'SY': 'Syrian Arab Republic', 
'KG': 'Kyrgyzstan', 'KE': 'Kenya', 'SR': 'Suriname', 'KI': 'Kiribati', 'KH': 'Cambodia', 'SV': 'El Salvador', 'KM': 'Comoros', 
'ST': 'Sao Tome and Principe', 'SK': 'Slovakia', 'KR': 'Korea, Republic of', 'SI': 'Slovenia', 'KP': "Korea, Democratic People's Republic of", 
'KW': 'Kuwait', 'SN': 'Senegal', 'SM': 'San Marino', 'SL': 'Sierra Leone', 'SC': 'Seychelles', 'KZ': 'Kazakhstan', 'KY': 'Cayman Islands', 
'SG': 'Singapore', 'SE': 'Sweden', 'SD': 'Sudan', 'DO': 'Dominican Republic', 'DM': 'Dominica', 'DJ': 'Djibouti', 'DK': 'Denmark', 
'VG': 'Virgin Islands, British', 'DE': 'Germany', 'YE': 'Yemen', 'DZ': 'Algeria', 'US': 'United States', 'UY': 'Uruguay', 
'YT': 'Mayotte', 'UM': 'United States Minor Outlying Islands', 'LB': 'Lebanon', 'LC': 'Saint Lucia', 'LA': "Lao People's Democratic Republic", 
'TV': 'Tuvalu', 'TW': 'Taiwan, Province of China', 'TT': 'Trinidad and Tobago', 'TR': 'Turkey', 'LK': 'Sri Lanka', 'LI': 'Liechtenstein', 
'LV': 'Latvia', 'TO': 'Tonga', 'LT': 'Lithuania', 'LU': 'Luxembourg', 'LR': 'Liberia', 'LS': 'Lesotho', 'TH': 'Thailand', 
'TF': 'French Southern Territories', 'TG': 'Togo', 'TD': 'Chad', 'TC': 'Turks and Caicos Islands', 'LY': 'Libyan Arab Jamahiriya', 
'VA': 'Holy See (Vatican City State)', 'VC': 'Saint Vincent and The Grenadines', 'AE': 'United Arab Emirates', 'AD': 'Andorra', 
'AG': 'Antigua and Barbuda', 'AF': 'Afghanistan', 'AI': 'Anguilla', 'VI': 'Virgin Islands, U.S.', 'IS': 'Iceland', 'IR': 'Iran, Islamic Republic of', 
'AM': 'Armenia', 'AL': 'Albania', 'AO': 'Angola', 'AN': 'Netherlands Antilles', 'AQ': 'Antarctica', 'AS': 'American Samoa', 'AR': 'Argentina', 
'AU': 'Australia', 'AT': 'Austria', 'IO': 'British Indian Ocean Territory', 'IN': 'India', 'AX': 'Aland Islands', 'AZ': 'Azerbaijan', 
'IE': 'Ireland', 'ID': 'Indonesia', 'UA': 'Ukraine', 'QA': 'Qatar', 'MZ': 'Mozambique'}

# parse /var/log/auth.log and find invalid attempts and create a list of IPs 
def get_ips_from_auth_log():
	path_to_auth_log = "/var/log/auth.log"#consider using glob to find all auth logs and add gzip support for compressed logs

	with open(path_to_auth_log,"r") as handle:
		ip_list_raw = [x.split()[-1].strip() for x in handle.readlines() if "Invalid" in x and "from" in x]

	ip_list = []
	#need to clean out duplicates here
	[ip_list.append(x) for x in ip_list_raw if x not in ip_list]
	return ip_list

#uses geoip2 to get country code for each ip
def fetch_country_from_ip(iplist_data):
	stats_dict = {}
	count2 = 0
	for ip in iplist_data:
		if geolite2.lookup(ip) != None:
			count2 += 1
			country = country_codes[geolite2.lookup(ip).country]
			if country not in stats_dict:
				stats_dict[country] = 1
			if country in stats_dict:
				stats_dict[country] += 1

	return [stats_dict, (len(iplist_data) - count2)]

ips = get_ips_from_auth_log()
stats = fetch_country_from_ip(ips)[0]
failed_to_identify_country = fetch_country_from_ip(ips)[1]#nice to see what is missed

#convert to tuples so we can sort from max to min
list_tuple = []
for key, value in stats.iteritems():
	list_tuple.append((key,value))

list_tuple.sort(key=lambda tup: tup[1], reverse=True)

line = "------------------------------------------------------------"

print line
for x in list_tuple:
	print str(x[0]) + " - " + str(x[1])
	print line
print "\n" + line
print "The location of " + str(failed_to_identify_country) + " IP address(s) was unsucessful."
print line

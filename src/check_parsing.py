from bs4 import BeautifulSoup
import sys
sys.stdout.reconfigure(encoding='utf-8')

html_cat = """
<div _ngcontent-storefront-c140="" role="region" class="breadcrumb-section" aria-label="首頁"><ol _ngcontent-storefront-c140="" class="breadcrumb ng-star-inserted"><li _ngcontent-storefront-c140="" class="ng-star-inserted"><a _ngcontent-storefront-c140="" title="首頁" href="/" class="ng-star-inserted"> 首頁 </a><!----><!----></li><li _ngcontent-storefront-c140="" class="ng-star-inserted"><a _ngcontent-storefront-c140="" title="保健美容" href="/Health-Beauty/c/7" class="ng-star-inserted"> 保健美容 </a><!----><!----></li><li _ngcontent-storefront-c140="" class="ng-star-inserted"><a _ngcontent-storefront-c140="" title="保健食品" href="/Health-Beauty/Supplements/c/701" class="ng-star-inserted"> 保健食品 </a><!----><!----></li><li _ngcontent-storefront-c140="" class="ng-star-inserted"><a _ngcontent-storefront-c140="" title="維他命" href="/Health-Beauty/Supplements/Multi-Letter-Vitamins/c/70101" class="ng-star-inserted"> 維他命 </a><!----><!----></li><!----></ol><!----><!----></div>
"""

soup_cat = BeautifulSoup(html_cat, 'html.parser')
breadcrumb_ol = soup_cat.select_one('ol.breadcrumb')
if breadcrumb_ol:
    cats = [a.get_text(strip=True) for a in breadcrumb_ol.select('a') if a.get_text(strip=True)]
    print("Category:", " > ".join(cats))
else:
    print("Failed to find category")

html_desc = """
<mat-expansion-panel hidetoggle="" class="mat-expansion-panel ng-tns-c241-11 ng-star-inserted mat-expanded" id="product_details"><mat-expansion-panel-header role="button" class="mat-expansion-panel-header mat-focus-indicator ng-tns-c242-15 ng-star-inserted mat-expanded" id="mat-expansion-panel-header-0" tabindex="0" aria-controls="cdk-accordion-child-0" aria-expanded="true" aria-disabled="false"><span class="mat-content ng-tns-c242-15 mat-content-hide-toggle"><mat-panel-title class="mat-expansion-panel-header-title ng-tns-c242-15"> 商品敍述 <!----></mat-panel-title><mat-panel-description class="mat-expansion-panel-header-description ng-tns-c242-15"><!----></mat-panel-description><mat-icon role="img" class="mat-icon notranslate mat-icon-no-color ng-star-inserted cds-icon icon-minus" aria-hidden="true" data-mat-icon-type="font" data-mat-icon-name="icon-minus" fonticon="icon-minus"></mat-icon><!----></span><!----></mat-expansion-panel-header><!----><div role="region" class="mat-expansion-panel-content ng-tns-c241-11 ng-trigger ng-trigger-bodyExpansion" id="cdk-accordion-child-0" aria-labelledby="mat-expansion-panel-header-0" style="visibility: visible;"><div class="mat-expansion-panel-body ng-tns-c241-11"><div class="ng-tns-c241-11"><div _ngcontent-storefront-c253="" tabindex="0" class="pdp-tabs-content ng-star-inserted" style="max-height: 14262.8px;"><div _ngcontent-storefront-c253=""><div _ngcontent-storefront-c253="" class="product-details-wrapper product-details-wrapper--overflow"><div _ngcontent-storefront-c253="" class="pdp-tab-content-body product-details-content-wrapper"><ul> <li>完整8種維生素B群</li> <li>鐵幫助氣色紅潤</li> <li>維生素C促進膠原蛋白形成</li> <li>維生素E抗氧化</li></ul><p>商品規格:</p></div></div></div></div></div></div></mat-expansion-panel>
"""

soup_desc = BeautifulSoup(html_desc, 'html.parser')
desc_elem = soup_desc.select_one('.product-details-content-wrapper') or soup_desc.select_one('.product-details-wrapper') or soup_desc.select_one('#product-details')
if desc_elem:
    print("Description:", desc_elem.get_text(separator=' ', strip=True)[:100])
else:
    print("Failed to find description")

html_specs = """
<mat-expansion-panel hidetoggle="" class="mat-expansion-panel ng-tns-c241-12 ng-star-inserted mat-expanded" id="product_specs"><mat-expansion-panel-header role="button" class="mat-expansion-panel-header mat-focus-indicator ng-tns-c242-16 ng-star-inserted mat-expanded" id="mat-expansion-panel-header-1" tabindex="0" aria-controls="cdk-accordion-child-1" aria-expanded="true" aria-disabled="false"><span class="mat-content ng-tns-c242-16 mat-content-hide-toggle"><mat-panel-title class="mat-expansion-panel-header-title ng-tns-c242-16"> 商品規格 <!----></mat-panel-title><mat-panel-description class="mat-expansion-panel-header-description ng-tns-c242-16"><!----></mat-panel-description><mat-icon role="img" class="mat-icon notranslate mat-icon-no-color ng-star-inserted cds-icon icon-minus" aria-hidden="true" data-mat-icon-type="font" data-mat-icon-name="icon-minus" fonticon="icon-minus"></mat-icon><!----></span><!----></mat-expansion-panel-header><!----><div role="region" class="mat-expansion-panel-content ng-tns-c241-12 ng-trigger ng-trigger-bodyExpansion" id="cdk-accordion-child-1" aria-labelledby="mat-expansion-panel-header-1" style="visibility: visible;"><div class="mat-expansion-panel-body ng-tns-c241-12"><div class="ng-tns-c241-12"><div _ngcontent-storefront-c253="" class="pdp-tabs-content ng-star-inserted" style=""><div _ngcontent-storefront-c253="" class="product-classification-wrapper pdp-tab-content-body"><p _ngcontent-storefront-c253=""></p><sip-product-classification _ngcontent-storefront-c253="" _nghost-storefront-c252="" class="ng-star-inserted"><div _ngcontent-storefront-c252="" class="ng-star-inserted"><div _ngcontent-storefront-c252="" class="headline ng-star-inserted"></div><table _ngcontent-storefront-c252="" class="table ng-star-inserted"><tbody _ngcontent-storefront-c252=""><tr _ngcontent-storefront-c252="" class="ng-star-inserted"><td _ngcontent-storefront-c252="" class="attrib">品名</td><td _ngcontent-storefront-c252="" class="attrib-val">克補+鐵加強錠200錠</td></tr><!----></tbody></table></div></sip-product-classification></div></div></div></div></mat-expansion-panel>
"""

soup_specs = BeautifulSoup(html_specs, 'html.parser')
specs_table = soup_specs.select_one('sip-product-classification table') or soup_specs.select_one('#product_specs table')

if specs_table:
    specs_data = []
    for tr in specs_table.select('tr'):
        key_elem = tr.select_one('.attrib')
        val_elem = tr.select_one('.attrib-val')
        if key_elem and val_elem:
            specs_data.append(f"{key_elem.get_text(strip=True)}: {val_elem.get_text(strip=True)}")
    print("Specs:", specs_data)
else:
    print("Failed to find specs")

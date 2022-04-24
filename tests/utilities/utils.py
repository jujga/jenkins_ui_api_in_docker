import json


class DriverForAllure:
    driver = None


payload = json.dumps([
                {
                    "operationName": "FavoriteListQuery",
                    "variables": {
                        "page": 1,
                        "perPage": 20,
                        "searchTerm": "",
                        "categoryId": None,
                        "companyId": None,
                        "isFresh": True
                    },
                    "query": "query FavoriteListQuery($perPage: Int!, $page: Int!, $searchTerm: String!, $categoryId: Int, $companyId: Int, $saleFilter: Boolean, $availFilter: Boolean, $isFresh: Boolean) {\n  favoriteList(\n    perPage: $perPage\n    page: $page\n    search: $searchTerm\n    categoryId: $categoryId\n    companyId: $companyId\n    saleFilter: $saleFilter\n    availFilter: $availFilter\n    isFresh: $isFresh\n  ) {\n    heartedProducts {\n      id\n      name\n      status\n      presence\n      sign\n      price\n      priceWithDiscount\n      ecProductPrices\n      isPresenceSure\n      groupId\n      productTypeKey\n      categoryId\n      categoryIds\n      currencyText\n      imageUrl(width: 1400, height: 1400)\n      sku\n      wholesalePrices {\n        price\n        priceCurrencyLocalized\n        minimumOrderQuantity\n        measureUnit\n        __typename\n      }\n      company {\n        id\n        name\n        isContentHidden\n        siteDisabled\n        reviewsCount\n        positiveReviewsPercent\n        opinionsCount\n        catalogUrl\n        siteUrl\n        catalogOpinionList\n        isCertified\n        isPortalChatVisible\n        isShoppingCartEnabled\n        city\n        frameMapUrl\n        address {\n          region_id\n          __typename\n        }\n        branches {\n          id\n          name\n          companyId\n          phone\n          mapUrl\n          address {\n            region_id\n            city\n            zipCode\n            street\n            regionText\n            country {\n              name\n              __typename\n            }\n            __typename\n          }\n          __typename\n        }\n        __typename\n      }\n      labels {\n        isNovaPoshtaAvailable\n        isNovaPoshtaWithPromShipping\n        isJustinWithPromShipping\n        isEvoPayEnabled\n        isSuccessfulPurchase\n        isPromShippingEnabled\n        __typename\n      }\n      supplyPeriod\n      isPriceFrom\n      residueStatus\n      residueColorStatus\n      __typename\n    }\n    allCategories {\n      id\n      caption\n      alias\n      __typename\n    }\n    allCompanies {\n      id\n      name\n      __typename\n    }\n    productCount\n    pagesCount\n    saleFiltAvail\n    availFiltAvail\n    isDefCurrencyOnly\n    __typename\n  }\n}\n"
                },
                {
                    "operationName": "besidaQuery",
                    "variables": {},
                    "query": "query besidaQuery {\n  besida {\n    cdn_url\n    desktop_v\n    mobile_v\n    is_besida_enabled\n    __typename\n  }\n}\n"
                }
            ])

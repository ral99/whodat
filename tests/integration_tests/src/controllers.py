from whodat.handler import url

@url('/golden/corn/')
class GoldenCornHandler:
    def get(self, request):
        return 'Lets get the golden corn!'

    def post(self, request):
        return 'Lets post the golden corn!'

@url('/metal/_/food/_/')
class MetalFoodHandler:
    def get(self, request, metal, food):
        return 'Lets get the %s %s!' % (metal, food)

    def post(self, request, metal, food):
        return 'Lets post the %s %s!' % (metal, food)

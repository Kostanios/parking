from NomeroffNet.BBoxNpPoints import getCvZoneRGB, convertCvZonesRGBtoBGR, reshapePoints
from NomeroffNet import textPostprocessing

def get_nomer (img, detector, npPointsCraft, optionsDetector, textDetector):
  # Detect numberplate
  targetBoxes = detector.detect_bbox(img)

  if len(targetBoxes) == 0:
    print("машин нет!")
    return
  all_points = npPointsCraft.detect(img, targetBoxes,[5,2,0])
  # cut zones
  zones = convertCvZonesRGBtoBGR([getCvZoneRGB(img, reshapePoints(rect, 1)) for rect in all_points])
  # predict zones attributes 
  regionIds, countLines = optionsDetector.predict(zones)
  regionNames = optionsDetector.getRegionLabels(regionIds)
  # find text with postprocessing by standart
  textArr = textDetector.predict(zones)
  textArr = textPostprocessing(textArr, regionNames)
  return textArr
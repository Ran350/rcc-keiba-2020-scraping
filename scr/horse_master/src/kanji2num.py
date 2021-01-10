def convert_kanji(zahl):
    japnumber = ("兆", "億",  "万")
    jap_factors = {
        "兆": 1000000000000,
        "億": 100000000,
        "万": 10000
    }

    zahl = zahl.replace(',', '')

    # Define the variables
    converted_number = 0
    already_found = False
    found_kanji_previous = 0

    # If the number can be returned as an integer (i.e. no Kanji in it) -> do it
    try:
        return(int(zahl))
    except ValueError:  # If not, disintegrate it
        for key in japnumber:  # do it for every Kanji
            if key in zahl:  # If it has been found in the original string:
                gef_kanji = zahl.find(key)  # mark, which Kanji has been found
                if not already_found:  # if it is the first kanji:
                    # Convert the number in front of the Kanji with the appropriate factor
                    intermediate_step = int(
                        zahl[:gef_kanji]) * jap_factors[key]
                    converted_number = intermediate_step
                    already_found = True
                    found_kanji_previous = gef_kanji
                else:  # for sll other kanjis
                    intermediate_step = int(
                        zahl[found_kanji_previous+1:gef_kanji]) * jap_factors[key]
                    converted_number = converted_number + intermediate_step  # sum them up
                    found_kanji_previous = gef_kanji

        if len(zahl) > (found_kanji_previous+1):
            converted_number = converted_number + \
                int(zahl[found_kanji_previous+1:])
        return converted_number


if __name__ == '__main__':
    # print(convert_kanji('18億5,684万'))
    pass

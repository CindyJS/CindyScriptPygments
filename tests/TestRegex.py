import re
import sys
import unittest

import CindyScriptPygments as C

if sys.version_info[0] >= 3:
    u = str
else:
    u = str


class TestRegex(unittest.TestCase):

    def shouldMatch(self, string, length = None):
        string = u(string)
        m = self.re.match(string)
        self.assertTrue(m, 'should match ' + repr(string))
        if length is None:
            length = len(string)
        self.assertEqual(length, m.end(0))

    def shouldNotMatch(self, string):
        string = u(string)
        m = self.re.match(string)
        self.assertFalse(m, 'should not match ' + repr(string))

    def test_reOps(self):
        self.re = re.compile(C.reOps)
        self.shouldNotMatch('')
        self.shouldMatch('+')
        self.shouldNotMatch('(')
        self.shouldMatch('|')
        self.shouldMatch(';')
        self.shouldMatch('\u2260')
        self.shouldMatch('~>=')

    def test_reNumber(self):
        self.re = re.compile(C.reNumber)
        self.shouldMatch('1.2')
        self.shouldMatch('1..2', 1)
        self.shouldMatch('1  . . 2', 1)
        self.shouldMatch('1  . * 2', 4)
        self.shouldMatch('1  .   2')
        self.shouldMatch('. 3')
        self.shouldMatch('.  1  e  +  2')
        self.shouldMatch('3  .  e  4')

    def test_unicodeLetters(self):
        self.re = re.compile(C.unicodeLetters)
        self.shouldMatch('a')
        self.shouldNotMatch('1')
        self.shouldNotMatch('.')
        self.shouldMatch('\u00F6')
        self.shouldNotMatch('\u00F7')
        self.shouldMatch('\u00F8')
        self.shouldMatch('\u02E4')
        self.shouldNotMatch('\u02E5')
        self.shouldMatch('\uFFDC')
        self.shouldNotMatch('\uFFDE')
        self.shouldMatch('\U00010000')
        self.shouldNotMatch('\U0001000C')
        self.shouldMatch('\U0002CEA0')
        self.shouldMatch('\U0002CEA1')
        self.shouldNotMatch('\U0002CEA2')
        self.shouldMatch('\U00013210')
        self.shouldNotMatch('\U00013579')

    def test_unicodeDecompression(self):
        # We could have pasted the fully decompressed regexp into the
        # source, but we prefer to keep the source small and have the
        # expanded version just in the unit tests.
        bmp = 'A-Za-z\xAA\xB5\xBA\xC0-\xD6\xD8-\xF6\xF8-\u02C1\u02C6-\u02D1\u02E0-\u02E4\u02EC\u02EE\u0370-\u0374\u0376\u0377\u037A-\u037D\u037F\u0386\u0388-\u038A\u038C\u038E-\u03A1\u03A3-\u03F5\u03F7-\u0481\u048A-\u052F\u0531-\u0556\u0559\u0561-\u0587\u05D0-\u05EA\u05F0-\u05F2\u0620-\u064A\u066E\u066F\u0671-\u06D3\u06D5\u06E5\u06E6\u06EE\u06EF\u06FA-\u06FC\u06FF\u0710\u0712-\u072F\u074D-\u07A5\u07B1\u07CA-\u07EA\u07F4\u07F5\u07FA\u0800-\u0815\u081A\u0824\u0828\u0840-\u0858\u08A0-\u08B4\u0904-\u0939\u093D\u0950\u0958-\u0961\u0971-\u0980\u0985-\u098C\u098F\u0990\u0993-\u09A8\u09AA-\u09B0\u09B2\u09B6-\u09B9\u09BD\u09CE\u09DC\u09DD\u09DF-\u09E1\u09F0\u09F1\u0A05-\u0A0A\u0A0F\u0A10\u0A13-\u0A28\u0A2A-\u0A30\u0A32\u0A33\u0A35\u0A36\u0A38\u0A39\u0A59-\u0A5C\u0A5E\u0A72-\u0A74\u0A85-\u0A8D\u0A8F-\u0A91\u0A93-\u0AA8\u0AAA-\u0AB0\u0AB2\u0AB3\u0AB5-\u0AB9\u0ABD\u0AD0\u0AE0\u0AE1\u0AF9\u0B05-\u0B0C\u0B0F\u0B10\u0B13-\u0B28\u0B2A-\u0B30\u0B32\u0B33\u0B35-\u0B39\u0B3D\u0B5C\u0B5D\u0B5F-\u0B61\u0B71\u0B83\u0B85-\u0B8A\u0B8E-\u0B90\u0B92-\u0B95\u0B99\u0B9A\u0B9C\u0B9E\u0B9F\u0BA3\u0BA4\u0BA8-\u0BAA\u0BAE-\u0BB9\u0BD0\u0C05-\u0C0C\u0C0E-\u0C10\u0C12-\u0C28\u0C2A-\u0C39\u0C3D\u0C58-\u0C5A\u0C60\u0C61\u0C85-\u0C8C\u0C8E-\u0C90\u0C92-\u0CA8\u0CAA-\u0CB3\u0CB5-\u0CB9\u0CBD\u0CDE\u0CE0\u0CE1\u0CF1\u0CF2\u0D05-\u0D0C\u0D0E-\u0D10\u0D12-\u0D3A\u0D3D\u0D4E\u0D5F-\u0D61\u0D7A-\u0D7F\u0D85-\u0D96\u0D9A-\u0DB1\u0DB3-\u0DBB\u0DBD\u0DC0-\u0DC6\u0E01-\u0E30\u0E32\u0E33\u0E40-\u0E46\u0E81\u0E82\u0E84\u0E87\u0E88\u0E8A\u0E8D\u0E94-\u0E97\u0E99-\u0E9F\u0EA1-\u0EA3\u0EA5\u0EA7\u0EAA\u0EAB\u0EAD-\u0EB0\u0EB2\u0EB3\u0EBD\u0EC0-\u0EC4\u0EC6\u0EDC-\u0EDF\u0F00\u0F40-\u0F47\u0F49-\u0F6C\u0F88-\u0F8C\u1000-\u102A\u103F\u1050-\u1055\u105A-\u105D\u1061\u1065\u1066\u106E-\u1070\u1075-\u1081\u108E\u10A0-\u10C5\u10C7\u10CD\u10D0-\u10FA\u10FC-\u1248\u124A-\u124D\u1250-\u1256\u1258\u125A-\u125D\u1260-\u1288\u128A-\u128D\u1290-\u12B0\u12B2-\u12B5\u12B8-\u12BE\u12C0\u12C2-\u12C5\u12C8-\u12D6\u12D8-\u1310\u1312-\u1315\u1318-\u135A\u1380-\u138F\u13A0-\u13F5\u13F8-\u13FD\u1401-\u166C\u166F-\u167F\u1681-\u169A\u16A0-\u16EA\u16F1-\u16F8\u1700-\u170C\u170E-\u1711\u1720-\u1731\u1740-\u1751\u1760-\u176C\u176E-\u1770\u1780-\u17B3\u17D7\u17DC\u1820-\u1877\u1880-\u18A8\u18AA\u18B0-\u18F5\u1900-\u191E\u1950-\u196D\u1970-\u1974\u1980-\u19AB\u19B0-\u19C9\u1A00-\u1A16\u1A20-\u1A54\u1AA7\u1B05-\u1B33\u1B45-\u1B4B\u1B83-\u1BA0\u1BAE\u1BAF\u1BBA-\u1BE5\u1C00-\u1C23\u1C4D-\u1C4F\u1C5A-\u1C7D\u1CE9-\u1CEC\u1CEE-\u1CF1\u1CF5\u1CF6\u1D00-\u1DBF\u1E00-\u1F15\u1F18-\u1F1D\u1F20-\u1F45\u1F48-\u1F4D\u1F50-\u1F57\u1F59\u1F5B\u1F5D\u1F5F-\u1F7D\u1F80-\u1FB4\u1FB6-\u1FBC\u1FBE\u1FC2-\u1FC4\u1FC6-\u1FCC\u1FD0-\u1FD3\u1FD6-\u1FDB\u1FE0-\u1FEC\u1FF2-\u1FF4\u1FF6-\u1FFC\u2071\u207F\u2090-\u209C\u2102\u2107\u210A-\u2113\u2115\u2119-\u211D\u2124\u2126\u2128\u212A-\u212D\u212F-\u2139\u213C-\u213F\u2145-\u2149\u214E\u2183\u2184\u2C00-\u2C2E\u2C30-\u2C5E\u2C60-\u2CE4\u2CEB-\u2CEE\u2CF2\u2CF3\u2D00-\u2D25\u2D27\u2D2D\u2D30-\u2D67\u2D6F\u2D80-\u2D96\u2DA0-\u2DA6\u2DA8-\u2DAE\u2DB0-\u2DB6\u2DB8-\u2DBE\u2DC0-\u2DC6\u2DC8-\u2DCE\u2DD0-\u2DD6\u2DD8-\u2DDE\u2E2F\u3005\u3006\u3031-\u3035\u303B\u303C\u3041-\u3096\u309D-\u309F\u30A1-\u30FA\u30FC-\u30FF\u3105-\u312D\u3131-\u318E\u31A0-\u31BA\u31F0-\u31FF\u3400-\u4DB5\u4E00-\u9FD5\uA000-\uA48C\uA4D0-\uA4FD\uA500-\uA60C\uA610-\uA61F\uA62A\uA62B\uA640-\uA66E\uA67F-\uA69D\uA6A0-\uA6E5\uA717-\uA71F\uA722-\uA788\uA78B-\uA7AD\uA7B0-\uA7B7\uA7F7-\uA801\uA803-\uA805\uA807-\uA80A\uA80C-\uA822\uA840-\uA873\uA882-\uA8B3\uA8F2-\uA8F7\uA8FB\uA8FD\uA90A-\uA925\uA930-\uA946\uA960-\uA97C\uA984-\uA9B2\uA9CF\uA9E0-\uA9E4\uA9E6-\uA9EF\uA9FA-\uA9FE\uAA00-\uAA28\uAA40-\uAA42\uAA44-\uAA4B\uAA60-\uAA76\uAA7A\uAA7E-\uAAAF\uAAB1\uAAB5\uAAB6\uAAB9-\uAABD\uAAC0\uAAC2\uAADB-\uAADD\uAAE0-\uAAEA\uAAF2-\uAAF4\uAB01-\uAB06\uAB09-\uAB0E\uAB11-\uAB16\uAB20-\uAB26\uAB28-\uAB2E\uAB30-\uAB5A\uAB5C-\uAB65\uAB70-\uABE2\uAC00-\uD7A3\uD7B0-\uD7C6\uD7CB-\uD7FB\uF900-\uFA6D\uFA70-\uFAD9\uFB00-\uFB06\uFB13-\uFB17\uFB1D\uFB1F-\uFB28\uFB2A-\uFB36\uFB38-\uFB3C\uFB3E\uFB40\uFB41\uFB43\uFB44\uFB46-\uFBB1\uFBD3-\uFD3D\uFD50-\uFD8F\uFD92-\uFDC7\uFDF0-\uFDFB\uFE70-\uFE74\uFE76-\uFEFC\uFF21-\uFF3A\uFF41-\uFF5A\uFF66-\uFFBE\uFFC2-\uFFC7\uFFCA-\uFFCF\uFFD2-\uFFD7\uFFDA-\uFFDC'
        if len('\U00012345') > 1:
            expected = '(?:[' + bmp + ']' + eval("""(
                u'|\uD800[\uDC00-\uDC0B\uDC0D-\uDC26\uDC28-\uDC3A\uDC3C\uDC3D\uDC3F-\uDC4D\uDC50-\uDC5D\uDC80-\uDCFA\uDE80-\uDE9C\uDEA0-\uDED0\uDF00-\uDF1F\uDF30-\uDF40\uDF42-\uDF49\uDF50-\uDF75\uDF80-\uDF9D\uDFA0-\uDFC3\uDFC8-\uDFCF]'
                u'|\uD801[\uDC00-\uDC9D\uDD00-\uDD27\uDD30-\uDD63\uDE00-\uDF36\uDF40-\uDF55\uDF60-\uDF67]'
                u'|\uD802[\uDC00-\uDC05\uDC08\uDC0A-\uDC35\uDC37\uDC38\uDC3C\uDC3F-\uDC55\uDC60-\uDC76\uDC80-\uDC9E\uDCE0-\uDCF2\uDCF4\uDCF5\uDD00-\uDD15\uDD20-\uDD39\uDD80-\uDDB7\uDDBE\uDDBF\uDE00\uDE10-\uDE13\uDE15-\uDE17\uDE19-\uDE33\uDE60-\uDE7C\uDE80-\uDE9C\uDEC0-\uDEC7\uDEC9-\uDEE4\uDF00-\uDF35\uDF40-\uDF55\uDF60-\uDF72\uDF80-\uDF91]'
                u'|\uD803[\uDC00-\uDC48\uDC80-\uDCB2\uDCC0-\uDCF2]'
                u'|\uD804[\uDC03-\uDC37\uDC83-\uDCAF\uDCD0-\uDCE8\uDD03-\uDD26\uDD50-\uDD72\uDD76\uDD83-\uDDB2\uDDC1-\uDDC4\uDDDA\uDDDC\uDE00-\uDE11\uDE13-\uDE2B\uDE80-\uDE86\uDE88\uDE8A-\uDE8D\uDE8F-\uDE9D\uDE9F-\uDEA8\uDEB0-\uDEDE\uDF05-\uDF0C\uDF0F\uDF10\uDF13-\uDF28\uDF2A-\uDF30\uDF32\uDF33\uDF35-\uDF39\uDF3D\uDF50\uDF5D-\uDF61]'
                u'|\uD805[\uDC80-\uDCAF\uDCC4\uDCC5\uDCC7\uDD80-\uDDAE\uDDD8-\uDDDB\uDE00-\uDE2F\uDE44\uDE80-\uDEAA\uDF00-\uDF19]'
                u'|\uD806[\uDCA0-\uDCDF\uDCFF\uDEC0-\uDEF8]'
                u'|\uD808[\uDC00-\uDF99]'
                u'|\uD809[\uDC80-\uDD43]'
                u'|\uD80D[\uDC00-\uDC2E]'
                u'|\uD811[\uDC00-\uDE46]'
                u'|\uD81A[\uDC00-\uDE38\uDE40-\uDE5E\uDED0-\uDEED\uDF00-\uDF2F\uDF40-\uDF43\uDF63-\uDF77\uDF7D-\uDF8F]'
                u'|\uD81B[\uDF00-\uDF44\uDF50\uDF93-\uDF9F]'
                u'|\uD82C[\uDC00\uDC01]'
                u'|\uD82F[\uDC00-\uDC6A\uDC70-\uDC7C\uDC80-\uDC88\uDC90-\uDC99]'
                u'|\uD835[\uDC00-\uDC54\uDC56-\uDC9C\uDC9E\uDC9F\uDCA2\uDCA5\uDCA6\uDCA9-\uDCAC\uDCAE-\uDCB9\uDCBB\uDCBD-\uDCC3\uDCC5-\uDD05\uDD07-\uDD0A\uDD0D-\uDD14\uDD16-\uDD1C\uDD1E-\uDD39\uDD3B-\uDD3E\uDD40-\uDD44\uDD46\uDD4A-\uDD50\uDD52-\uDEA5\uDEA8-\uDEC0\uDEC2-\uDEDA\uDEDC-\uDEFA\uDEFC-\uDF14\uDF16-\uDF34\uDF36-\uDF4E\uDF50-\uDF6E\uDF70-\uDF88\uDF8A-\uDFA8\uDFAA-\uDFC2\uDFC4-\uDFCB]'
                u'|\uD83A[\uDC00-\uDCC4]'
                u'|\uD83B[\uDE00-\uDE03\uDE05-\uDE1F\uDE21\uDE22\uDE24\uDE27\uDE29-\uDE32\uDE34-\uDE37\uDE39\uDE3B\uDE42\uDE47\uDE49\uDE4B\uDE4D-\uDE4F\uDE51\uDE52\uDE54\uDE57\uDE59\uDE5B\uDE5D\uDE5F\uDE61\uDE62\uDE64\uDE67-\uDE6A\uDE6C-\uDE72\uDE74-\uDE77\uDE79-\uDE7C\uDE7E\uDE80-\uDE89\uDE8B-\uDE9B\uDEA1-\uDEA3\uDEA5-\uDEA9\uDEAB-\uDEBB]'
                u'|\uD869[\uDC00-\uDED6\uDF00-\uDFFF]'
                u'|\uD86D[\uDC00-\uDF34\uDF40-\uDFFF]'
                u'|\uD86E[\uDC00-\uDC1D\uDC20-\uDFFF]'
                u'|\uD873[\uDC00-\uDEA1]'
                u'|\uD87E[\uDC00-\uDE1D]'
                u'|[\uD80C\uD840-\uD868\uD86A-\uD86C\uD86F-\uD872][\uDC00-\uDFFF]'
                u')'
            )""")
        else:
            expected = (
                '[' + bmp +
                '\U00010000-\U0001000B\U0001000D-\U00010026\U00010028-\U0001003A\U0001003C\U0001003D\U0001003F-\U0001004D\U00010050-\U0001005D\U00010080-\U000100FA\U00010280-\U0001029C\U000102A0-\U000102D0\U00010300-\U0001031F\U00010330-\U00010340\U00010342-\U00010349\U00010350-\U00010375\U00010380-\U0001039D\U000103A0-\U000103C3\U000103C8-\U000103CF'
                '\U00010400-\U0001049D\U00010500-\U00010527\U00010530-\U00010563\U00010600-\U00010736\U00010740-\U00010755\U00010760-\U00010767'
                '\U00010800-\U00010805\U00010808\U0001080A-\U00010835\U00010837\U00010838\U0001083C\U0001083F-\U00010855\U00010860-\U00010876\U00010880-\U0001089E\U000108E0-\U000108F2\U000108F4\U000108F5\U00010900-\U00010915\U00010920-\U00010939\U00010980-\U000109B7\U000109BE\U000109BF\U00010A00\U00010A10-\U00010A13\U00010A15-\U00010A17\U00010A19-\U00010A33\U00010A60-\U00010A7C\U00010A80-\U00010A9C\U00010AC0-\U00010AC7\U00010AC9-\U00010AE4\U00010B00-\U00010B35\U00010B40-\U00010B55\U00010B60-\U00010B72\U00010B80-\U00010B91'
                '\U00010C00-\U00010C48\U00010C80-\U00010CB2\U00010CC0-\U00010CF2'
                '\U00011003-\U00011037\U00011083-\U000110AF\U000110D0-\U000110E8\U00011103-\U00011126\U00011150-\U00011172\U00011176\U00011183-\U000111B2\U000111C1-\U000111C4\U000111DA\U000111DC\U00011200-\U00011211\U00011213-\U0001122B\U00011280-\U00011286\U00011288\U0001128A-\U0001128D\U0001128F-\U0001129D\U0001129F-\U000112A8\U000112B0-\U000112DE\U00011305-\U0001130C\U0001130F\U00011310\U00011313-\U00011328\U0001132A-\U00011330\U00011332\U00011333\U00011335-\U00011339\U0001133D\U00011350\U0001135D-\U00011361'
                '\U00011480-\U000114AF\U000114C4\U000114C5\U000114C7\U00011580-\U000115AE\U000115D8-\U000115DB\U00011600-\U0001162F\U00011644\U00011680-\U000116AA\U00011700-\U00011719'
                '\U000118A0-\U000118DF\U000118FF\U00011AC0-\U00011AF8'
                '\U00012000-\U00012399'
                '\U00012480-\U00012543'
                '\U00013400-\U0001342E'
                '\U00014400-\U00014646'
                '\U00016800-\U00016A38\U00016A40-\U00016A5E\U00016AD0-\U00016AED\U00016B00-\U00016B2F\U00016B40-\U00016B43\U00016B63-\U00016B77\U00016B7D-\U00016B8F'
                '\U00016F00-\U00016F44\U00016F50\U00016F93-\U00016F9F'
                '\U0001B000\U0001B001'
                '\U0001BC00-\U0001BC6A\U0001BC70-\U0001BC7C\U0001BC80-\U0001BC88\U0001BC90-\U0001BC99'
                '\U0001D400-\U0001D454\U0001D456-\U0001D49C\U0001D49E\U0001D49F\U0001D4A2\U0001D4A5\U0001D4A6\U0001D4A9-\U0001D4AC\U0001D4AE-\U0001D4B9\U0001D4BB\U0001D4BD-\U0001D4C3\U0001D4C5-\U0001D505\U0001D507-\U0001D50A\U0001D50D-\U0001D514\U0001D516-\U0001D51C\U0001D51E-\U0001D539\U0001D53B-\U0001D53E\U0001D540-\U0001D544\U0001D546\U0001D54A-\U0001D550\U0001D552-\U0001D6A5\U0001D6A8-\U0001D6C0\U0001D6C2-\U0001D6DA\U0001D6DC-\U0001D6FA\U0001D6FC-\U0001D714\U0001D716-\U0001D734\U0001D736-\U0001D74E\U0001D750-\U0001D76E\U0001D770-\U0001D788\U0001D78A-\U0001D7A8\U0001D7AA-\U0001D7C2\U0001D7C4-\U0001D7CB'
                '\U0001E800-\U0001E8C4'
                '\U0001EE00-\U0001EE03\U0001EE05-\U0001EE1F\U0001EE21\U0001EE22\U0001EE24\U0001EE27\U0001EE29-\U0001EE32\U0001EE34-\U0001EE37\U0001EE39\U0001EE3B\U0001EE42\U0001EE47\U0001EE49\U0001EE4B\U0001EE4D-\U0001EE4F\U0001EE51\U0001EE52\U0001EE54\U0001EE57\U0001EE59\U0001EE5B\U0001EE5D\U0001EE5F\U0001EE61\U0001EE62\U0001EE64\U0001EE67-\U0001EE6A\U0001EE6C-\U0001EE72\U0001EE74-\U0001EE77\U0001EE79-\U0001EE7C\U0001EE7E\U0001EE80-\U0001EE89\U0001EE8B-\U0001EE9B\U0001EEA1-\U0001EEA3\U0001EEA5-\U0001EEA9\U0001EEAB-\U0001EEBB'
                '\U0002A400-\U0002A6D6\U0002A700-\U0002A7FF'
                '\U0002B400-\U0002B734\U0002B740-\U0002B7FF'
                '\U0002B800-\U0002B81D\U0002B820-\U0002BBFF'
                '\U0002CC00-\U0002CEA1'
                '\U0002F800-\U0002FA1D'
                '\U00013000-\U000133FF\U00020000-\U0002A3FF\U0002A800-\U0002B3FF\U0002BC00-\U0002CBFF'
                ']')
        actual = C.unicodeLetters
        if expected == actual:
            return None
        expected = expected.encode("unicode_escape").decode("ascii")
        actual = actual.encode("unicode_escape").decode("ascii")
        i = 10
        while expected[:i] == actual[:i]:
            i += 1
        e = expected[i - 10 : i + 10]
        a = actual[i - 10 : i + 10]
        self.assertEqual(e, a, "'{0}{1}{2}' != '{0}{3}{4}'".format(
            '' if i - 10 <= 0 else '...',
            e, '' if i + 10 >= len(expected) else '...',
            a, '' if i + 10 >= len(actual) else '...',
        ))



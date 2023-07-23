import json

normalSigners = [
    {
        "publicKey":  "0xB320Ec919373456Cf20f93115ABF4cb304F3f674",
        "privateKey": "0x86905c9ef0fd5a73ea848be78aebdf8899dd792e1431a21b715117faabe2c0c9",
    },
]

blsSigners = [
    {
        "secret": 46337422815165563069770,
        "x1": 10706095686698245787932975467861938220625018575176472970844756047036360626836,
        "x2": 8662663408394575674460701006639858888902536624848243691663778607982930620726,
        "y1": 14094584621742845231021041520832018581730738887502313740807797453480045434743,
        "y2": 9068888814553294278287895706250595211030348008114977585542249661279489519854,
    },
    {
        "secret": 36482904330669657465867,
        "x1": 13747230360591626995841744679376708613551353261686305295863641576968757320156,
        "x2": 20316111933070948253839161994045364387477989086253390425492493699072731744847,
        "y1": 9751519789290653819679754713086735608201366167232038313616846293580794795186,
        "y2": 20465084893242271293439816868873631582941277041932998943978718687328391166054,
    },
    {
        "secret": 24288943331878747621714,
        "x1": 12979772211372237823564767605330108862981102167089408355144884142119809681284,
        "x2": 3284788267748721533338167687175978023669752620846822484230549832696356633549,
        "y1": 11951973789181162248208681968437670181222221687138438530902771998336017891330,
        "y2": 4298773631589319273681890041707268591087047798831671455944101989233276819449,
    },
    {
        "secret": 16778097771267239626366353994059100715857512226821280121159725862462254995695,
        "x1": 935211787151325400799498085673696799120282505895217489467242895712759815928,
        "x2": 15169088789998255762179172207415058200150231209137374768709656222774158184423,
        "y1": 6600247568639493533124623953993877695841883183710449813396223878095345591699,
        "y2": 7658899368928833780572304029911245535984334316141799205842095425854219533354,
    },
    {
        "secret": 3851559670588668594581683731771106941494831330773534803535573266760943238947,
        "x1": 20104072164784975967714638011929971261183946392318581784648726560236075603564,
        "x2": 4519086635449012842993265768071828444429031142601242442223461806948762598205,
        "y1": 17754816334603441952934715594709739861039692565488118254263731632105100427401,
        "y2": 824519930380102429689107677391338391691141887582944806618443386865798707070,
    },
    {
        "secret": 2333258750698608528326167445275753793875624234268221942070301476062217224931,
        "x1": 7238719488660391687619845516401701897123352982032990741242002018642725686291,
        "x2": 11688369308864947228624927375818105664059391046122168972585772479118920978831,
        "y1": 5139637010805550737284187370417977032772936117766032098440093561208727691173,
        "y2": 8240519580952175624734496195360093713481116252928102222625824477117658445040,
    },
    {
        "secret": 19901191875454150926515027318114560177735480128850790487922309923732624807311,
        "x1": 12379933196838491511456676772269271308491457067611968533162356327786008858487,
        "x2": 9567226171601256369752148525431982154446674085737522220030191044999450700236,
        "y1": 7858040560004767811350427452306909771380042919840416047641062482119108524212,
        "y2": 14880772881098733914696093510223020021670365408569382422047819077653966603349,
    },
]

wallets = {
    "wallet-1": {
        "address": "0xC5fc9E0606987b202a8C3756E110f383A9587caf",
    },
    "wallet-2": {
        "address": "0x88651B69c1A167E7339efCAFbCdB2b2cD2134194"
    },
    "wallet-3": {
        "address": "0x9E803b23EA4CB8366D424FE964A506C02dab700e"
    },
    "wallet-4": {
        "address": "0x494841811e3Bab6925C50B1b80F525458691Fa2C"
    }
}

_safe_abi_file = open('./abis/safe.abi.json')
safe_abi = json.load(_safe_abi_file)

_aggregation_module_abi_file = open('./abis/aggregation_auth_module.abi.json')
aggregation_auth_abi = json.load(_aggregation_module_abi_file)

_bls_open_abi_file = open('./abis/bls_open.abi.json')
bls_open_abi = json.load(_bls_open_abi_file)

_aggregator_abi_file = open('./abis/aggregator.abi.json')
aggregator_abi = json.load(_aggregator_abi_file)

bls_open_address = "0xAa0599ccEF72f0624FaF004F398ceD5813128056"
aggregator_address = "0xe92dE7160b9Ab1c0239FA9c6A880624ABfCF0279"
aggregation_auth_module_address = "0x55758A3316D9fbe59153013FB8109Bc32cFb1E63"
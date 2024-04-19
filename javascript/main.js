function cleanString(input) {
    var output = "";
    for (var i=0; i<input.length; i++) {
        if (input.charCodeAt(i) <= 127) {
            output += input.charAt(i);
        } else {
            output += "_";
        }
    }
    return output;
}

let input = "Aa kiu, I swd skieo 236587. GH kiu: sieo?? 25.33";
let output = cleanString(input);
console.log(output); // Aa kiu, I swd skieo 236587. GH kiu: sieo?? 25.33

input = "Aa kiu, I swd skieo 236587. GH kiu: sieo?? 25.33 你好 世界 你好 世界 Ш, ш, ша [ʂa/sh], ша [ʂa], /ʃ/ o /ʂ";
output = cleanString(input);
console.log(output); // Aa kiu, I swd skieo 236587. GH kiu: sieo?? 25.33
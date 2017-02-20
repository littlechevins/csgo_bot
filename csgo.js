// This program is free software: you can redistribute it and/or modify
// it under the terms of the GNU General Public License as published by
// the Free Software Foundation, either version 3 of the License, or
// (at your option) any later version.

// Written by Kevin Luo
// 17.2.17
// v0.1

// For me
// reservationID is outcomeID

/******************************** 
*								*
*			Initiation		   	*
*								*
********************************/

var Steam = require("steam"),
    util = require("util"),
    fs = require("fs"),
    csgo = require("../"),
    bot = new Steam.SteamClient(),
    steamUser = new Steam.SteamUser(bot),
    steamFriends = new Steam.SteamFriends(bot),
    steamGC = new Steam.SteamGameCoordinator(bot, 730);
    CSGOCli = new csgo.CSGOClient(steamUser, steamGC, false),
    readlineSync = require("readline-sync"),
    crypto = require("crypto");


/********************************
*								*
*		Decode sharecode        *
*								*
********************************/

var scDecoder = new csgo.SharecodeDecoder("CSGO-U6MWi-hYFWJ-opPwD-JciHm-qOijD");
console.log("Sharecode CSGO-U6MWi-hYFWJ-opPwD-JciHm-qOijD decodes into: ");
console.log(scDecoder.decode());

// Hash encryption
function MakeSha(bytes) {
    var hash = crypto.createHash('sha1');
    hash.update(bytes);
    return hash.digest();
}


/********************************
*								*
*	What to do on Login         *
*								*
********************************/

var onSteamLogOn = function onSteamLogOn(response){
	if(response.eresult == Steam.EResult.OK){
		util.log('Logged in!');
	}else{
		util.log('Error, ', response);
		process.exit();
	}
	steamFriends.setPersonaState(Steam.EPersonaState.Busy);				// Set state to active
	util.log("Logged on");
	util.log("current SteamID64: "  + bot.steamID);
	util.log("Account ID: " + CSGOCli.ToAccountID(bot.steamID));

	CSGOCli.launch();														// Intiates instance of csgo

	CSGOCli.on("unhandled", function(message) {
		util.log("Unhandled msg");
		util.log(message);
	});

	CSGOCli.on("ready", function() {
		util.log("node-csgo ready.");

		CSGOCli.playerProfileRequest(CSGOCli.ToAccountID(bot.steamID));		// Gets current rank (lol noob)	
		CSGOCli.on("playerProfile", function(profile) {
			console.log("Profile");
			console.log("Player Rank: " + CSGOCli.Rank.getString(profile.account_profiles[0].ranking.rank_id));
			console.log(JSON.stringify(profile, null, 2));
		});

		CSGOCli.requestRecentGames(CSGOCli.ToAccountID(bot.steamID));										// Gets match ID's for 8 recent games
		CSGOCli.on("matchList", function(list) {
			console.log("Match List");
			if(list.matches && list.matches.length > 0){
				// console.log(list.matches[0])
				fs.writeFileSync('recentGamesLog.txt', JSON.stringify(list, null, 2));
				fs.writeFileSync('recentGamesLogArray.txt', list.matches[0]);
				console.log(JSON.stringify(list, null, 2));

			}
		});
	});

	CSGOCli.on("unready", function onUnready(){
		util.log("node-csgo unready.");
	});

	CSGOCli.on("unhandled", function(kMsg){
		util.log("UNHANDLED MESSAGE " + kMsg);
	});
},

onSteamSentry = function onSteamSentry(sentry){
	util.log("Received sentry.");
	require('fs').writeFileSync('sentry', sentry);
},
onSteamServers = function onSteamServers(servers){
	util.log("Received servers.");
	fs.writeFileSync('servers.json', JSON.stringify(servers, null, 2));
}

/********************************
*								*
*			Login         		*
*								*
********************************/
var username = readlineSync.question('Username: ');
var password = readlineSync.question('Password: ', {noEchoBack: true});
var authCode = readlineSync.question('AuthCode: ');

var logOnDetails = {
    "account_name": username,
    "password": password,
};
if (authCode !== "") {
    logOnDetails.two_factor_code = authCode;
}
var sentry = fs.readFileSync('sentry');
if (sentry.length) {
    logOnDetails.sha_sentryfile = MakeSha(sentry);
}
bot.connect();
steamUser.on('updateMachineAuth', function(response, callback){
    fs.writeFileSync('sentry', response.bytes);
    callback({ sha_file: MakeSha(response.bytes) });
});
bot.on("logOnResponse", onSteamLogOn)
    .on('sentry', onSteamSentry)
    .on('servers', onSteamServers)
    .on('connected', function(){
        steamUser.logOn(logOnDetails);
    });

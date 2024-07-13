"""
Configuration module for NHL Stats Dashboard.
Contains the list of relevant statistics for each position and team-color mapping.
"""

# Select relevant stats for each position
skater_stats= [
    'games_played','icetime','shifts','gameScore','onIce_xGoalsPercentage','offIce_xGoalsPercentage',
    'onIce_corsiPercentage','offIce_corsiPercentage','onIce_fenwickPercentage','offIce_fenwickPercentage',
    'iceTimeRank','I_F_xOnGoal','I_F_xGoals','I_F_xRebounds','I_F_xFreeze','I_F_xPlayStopped',
    'I_F_xPlayContinuedInZone','I_F_xPlayContinuedOutsideZone','I_F_flurryAdjustedxGoals',
    'I_F_scoreVenueAdjustedxGoals','I_F_flurryScoreVenueAdjustedxGoals','I_F_primaryAssists',
    'I_F_secondaryAssists','I_F_shotsOnGoal','I_F_missedShots','I_F_blockedShotAttempts',
    'I_F_shotAttempts','I_F_points','I_F_goals','I_F_rebounds','I_F_reboundGoals','I_F_freeze',
    'I_F_playStopped','I_F_playContinuedInZone','I_F_playContinuedOutsideZone','I_F_savedShotsOnGoal',
    'I_F_savedUnblockedShotAttempts','penalties','I_F_penalityMinutes','I_F_faceOffsWon,I_F_hits',
    'I_F_takeaways','I_F_giveaways','I_F_lowDangerShots','I_F_mediumDangerShots','I_F_highDangerShots',
    'I_F_lowDangerxGoals','I_F_mediumDangerxGoals','I_F_highDangerxGoals','I_F_lowDangerGoals',
    'I_F_mediumDangerGoals','I_F_highDangerGoals','I_F_scoreAdjustedShotsAttempts','I_F_unblockedShotAttempts',
    'I_F_scoreAdjustedUnblockedShotAttempts','I_F_dZoneGiveaways','I_F_xGoalsFromxReboundsOfShots',
    'I_F_xGoalsFromActualReboundsOfShots','I_F_reboundxGoals','I_F_xGoals_with_earned_rebounds',
    'I_F_xGoals_with_earned_rebounds_scoreAdjusted','I_F_xGoals_with_earned_rebounds_scoreFlurryAdjusted',
    'I_F_shifts','I_F_oZoneShiftStarts','I_F_dZoneShiftStarts','I_F_neutralZoneShiftStarts','I_F_flyShiftStarts',
    'I_F_oZoneShiftEnds','I_F_dZoneShiftEnds','I_F_neutralZoneShiftEnds','I_F_flyShiftEnds','faceoffsWon',
    'faceoffsLost','timeOnBench','penalityMinutes','penalityMinutesDrawn','penaltiesDrawn','shotsBlockedByPlayer',
    'OnIce_F_xOnGoal','OnIce_F_xGoals','OnIce_F_flurryAdjustedxGoals','OnIce_F_scoreVenueAdjustedxGoals',
    'OnIce_F_flurryScoreVenueAdjustedxGoals','OnIce_F_shotsOnGoal','OnIce_F_missedShots','OnIce_F_blockedShotAttempts','OnIce_F_shotAttempts',
    'OnIce_F_goals','OnIce_F_rebounds','OnIce_F_reboundGoals','OnIce_F_lowDangerShots','OnIce_F_mediumDangerShots',
    'OnIce_F_highDangerShots','OnIce_F_lowDangerxGoals','OnIce_F_mediumDangerxGoals','OnIce_F_highDangerxGoals',
    'OnIce_F_lowDangerGoals','OnIce_F_mediumDangerGoals','OnIce_F_highDangerGoals','OnIce_F_scoreAdjustedShotsAttempts',
    'OnIce_F_unblockedShotAttempts','OnIce_F_scoreAdjustedUnblockedShotAttempts','OnIce_F_xGoalsFromxReboundsOfShots',
    'OnIce_F_xGoalsFromActualReboundsOfShots','OnIce_F_reboundxGoals','OnIce_F_xGoals_with_earned_rebounds',
    'OnIce_F_xGoals_with_earned_rebounds_scoreAdjusted','OnIce_F_xGoals_with_earned_rebounds_scoreFlurryAdjusted',
    'OnIce_A_xOnGoal','OnIce_A_xGoals','OnIce_A_flurryAdjustedxGoals','OnIce_A_scoreVenueAdjustedxGoals',
    'OnIce_A_flurryScoreVenueAdjustedxGoals','OnIce_A_shotsOnGoal','OnIce_A_missedShots,OnIce_A_blockedShotAttempts',
    'OnIce_A_shotAttempts','OnIce_A_goals,OnIce_A_rebounds','OnIce_A_reboundGoals','OnIce_A_lowDangerShots',
    'OnIce_A_mediumDangerShots','OnIce_A_highDangerShots','OnIce_A_lowDangerxGoals','OnIce_A_mediumDangerxGoals',
    'OnIce_A_highDangerxGoals','OnIce_A_lowDangerGoals','OnIce_A_mediumDangerGoals','OnIce_A_highDangerGoals',
    'OnIce_A_scoreAdjustedShotsAttempts','OnIce_A_unblockedShotAttempts','OnIce_A_scoreAdjustedUnblockedShotAttempts',
    'OnIce_A_xGoalsFromxReboundsOfShots','OnIce_A_xGoalsFromActualReboundsOfShots','OnIce_A_reboundxGoals',
    'OnIce_A_xGoals_with_earned_rebounds','OnIce_A_xGoals_with_earned_rebounds_scoreAdjusted',
    'OnIce_A_xGoals_with_earned_rebounds_scoreFlurryAdjusted','OffIce_F_xGoals','OffIce_A_xGoals,OffIce_F_shotAttempts',
    'OffIce_A_shotAttempts','xGoalsForAfterShifts','xGoalsAgainstAfterShifts','corsiForAfterShifts','corsiAgainstAfterShifts',
    'fenwickForAfterShifts','fenwickAgainstAfterShifts'
]

# List to map the main color for each NFL team
teams_color = {
    'ANA': '#F47A38', 
    'ARI': '#8C2633',
    'BOS': '#FFB81C', 
    'BUF': '#003087', 
    'CGY': '#D2001C', 
    'CAR': '#CE1126', 
    'CHI': '#CF0A2C', 
    'COL': '#6F263D', 
    'CBJ': '#002654', 
    'DAL': '#006847', 
    'DET': '#CE1126', 
    'EDM': '#041E42', 
    'FLA': '#041E42', 
    'LAK': '#111111', 
    'MIN': '#154734', 
    'MTL': '#AF1E2D', 
    'NSH': '#FFB81C', 
    'NJD': '#CE1126', 
    'NYI': '#00539B', 
    'NYR': '#0038A8', 
    'OTT': '#DA1A32', 
    'PHI': '#F74902', 
    'PIT': '#FCB514', 
    'STL': '#002F87', 
    'SJS': '#006D75', 
    'SEA': '#001628', 
    'TBL': '#002868', 
    'TOR': '#00205B', 
    'VAN': '#00205B', 
    'VGK': '#B4975A', 
    'WSH': '#C8102E', 
    'WPG': '#041E42'
}
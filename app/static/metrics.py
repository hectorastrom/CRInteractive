from app.helpers import MetricText
# MetricTexts have format tag, name, description. Descriptions are default "" so they can be omitted.
rower_metric_list = [
    MetricText("gt", "General Technique", "Coaches' subjective estimate of your technique."),
    MetricText("bp", "Body Preparation", "Are arms fully extended, lats slightly engaged, spine supported, and shoulders forward of hips prior to quarter slide?"),
    MetricText("rhythm", "Rhythm", "Distance Over Time = Speed. Distance = Connected Length. Power * Connected Length = Distance Over Time."),
    MetricText("sync", "Synchronicity", "Doing the same thing as everyone else at the same time."),
    MetricText("enspd", "Entry Speed", "The time it takes for your blade to go from piercing the water’s surface to being at the optimal depth (top edge just under surface). Theoretically, perfect entry occurs at full arc, a.k.a. the point of farthest reach."),
    MetricText("drvmech", "Drive Mechanics", "Does the force you apply to the footboard move the boat and the rowers in it forwards or backwards?"),
    MetricText("bldlock", "Blade Lock", "Does your blade stay at the same depth throughout the whole drive?"),
    MetricText("release", "Release", "Do you complete the drive before feathering or applying downward pressure on the handle? Is the pressure off the blade before you remove it from the water?"),
    MetricText("hands", "Hands", "Do you use your inside wrist for the feather completely, or do you let the oarlock take over? Is your inside hand and arm relaxed when you square the blade and take the catch?"),
    MetricText("gp", "General Physiology", "Overall, less precise measure of physiology."),
    MetricText("pe", "Power Endurance", "Box jumps, bat mans, KB swings, pull-ups, truck pushes, 2k erg etc."),
    MetricText("ae", "Aerobic Endurance", "Stadium times, consistency in long rows, bi- or tri-athlons: anything longer than 20 minutes."),
    MetricText("mob", "Mobility", "Full range of motion at the ankle, knee, hip, shoulder without compensatory movement anywhere else in your body, especially in your spine."),
    MetricText("bm", "Breath Mechanics", "Do you maintain core stability when you’re breathing hard, or not? Are you able to remain un-shrugged all throughout long rows?")
]

cox_metric_list = [
    MetricText("pe", "Practice Efficiency", "Duration of practice transitions, getting boats on and off racks/water, spinning/aligning boats done without wasting time."),
    MetricText("pex", "Practice Execution", "Is your crew executing the prescribed drills properly on the first try? Do you rotate through pairs in sync with the coaches' and other boats' clocks? Is your crew at the prescribed rates the entire time?"),
    MetricText("tex", "Technical Execution", "How do your blades look? Are they skying? Missing water? Staying locked at the right depth? Are your stations catching and finishing together? Is your crew checking the boat, or picking it up on the fly?"),
    MetricText("st", "Steering", "Do you stay close to the other eight (when applicable)? Do you know how to maneuver around obstacles without disrupting the flow of practice? Do you stay on the right side of the river at all times?"),
    MetricText("candc", "Clarity and Conciceness", "In how few words are you able to get your message across? How easy is it for your crew to understand your commands? Is there unnecessary, meaningless filler?"),
]
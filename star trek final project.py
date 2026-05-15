from drafter import *
from bakery import assert_equal
from dataclasses import dataclass
from random import randint

@dataclass
class State:
    user_role: str
    user_name: str
    user_full_name: str
    message: str
    last_location: str
    pockets: list[str]
    fixed_terminal: bool
    starfleet_code: str
    lounge_searched:bool
    fixed_reactor_core:bool
    engineering_searched:bool
    crate2_searched:bool
    crate3_searched:bool
    elevator_searched:bool
    box1_searched:bool
    box3_searched:bool
    bar_searched:bool
    quarter1_fixed:bool
    quarter2_fixed:bool
    quarter1_searched:bool
    quarter2_searched:bool
    armory_searched:bool
    player_current_health:int
    player_max_health:int
    player_max_damage:int
    player_armor:int
    player_damage_buff:int
    total_objectives_complete:int
    total_enemies_defeated:int
    remaining_heals:int
    equipped_weapon: str
    equipped_armor: str
    current_burn_value: int
    phaser_setting: str
    current_total_drinks: int
    enemy_1_health: int
    enemy_2_health: int
    enemy_3_health: int
    enemy_4_health: int
    enemy_5_health: int
    current_enemy: int
    enemy_1_defeated: bool
    enemy_2_defeated: bool
    enemy_3_defeated: bool
    enemy_4_defeated: bool
    enemy_5_defeated: bool
    jail_searched: bool
    transporter_used: bool

initial_state = State('','','','','',[],False,'',False,False,False,False,False,False,False,False,False,False,False,False,False,False,0,0,0,0,0,0,0,3,'Hands','Starfleet Uniform',0,'Standard',0,20,20,20,20,20,0,False,False,False,False,False,False,False)

@route
def index(state:State)->Page:
    #game priming portion
    initial_code = randint(0,999999)
    strung_code = str(initial_code)
    if len(strung_code) == 6:
        state.starfleet_code = strung_code
    else:
        strung_code = strung_code.zfill(6)
        state.starfleet_code = strung_code
    #actual code portion
    return Page(state, content=[
        Header('Star Trek Repair'),
        "We were in battle, and our ship has been boarded and damaged. We need YOU to help us out!",
        "First, what's your name?",
        TextBox('rename'),
        Button('Confirm Name', name_change)
    ])

@route
def pockets(state:State)->Page:
    content_list = [Header('Pockets')]
    if not state.pockets:
        content_list.append("Your pockets are empty.")
    else:
        content_list.extend(state.pockets)
    content_list.append(Button('Stop Checking Pockets', state.last_location, margin_right=87))
    content_list.append(float_right(Button('View Player Card', player_card, margin_right=5)))
    content_list.append(float_right(Button('Equip Items', equipping_items, margin_right=5)))
    if 'Life Boost' in state.pockets:
        content_list.append(Button('Use Life Boost', use_life_boost, margin_left=-87))
    if 'Strength Boost' in state.pockets:
        content_list.append(Button('Use Strength Boost', use_strength_boost, margin_left=-87))
    if state.user_role == 'Engineer ':
        if 'Basic Phaser' in state.pockets:
            if 'Terminal Code Note' in state.pockets:
                content_list.append(Button('Change Phaser Setting', change_phaser_mode, margin_right=5))
            elif 'Terminal Code Note' not in state.pockets:
                content_list.append(Button('Change Phaser Mode', change_phaser_mode))
    if 'Terminal Code Note' in state.pockets:
        content_list.append(LineBreak())
        content_list.append(' ')
        content_list.append(Button('Read Terminal Code Note', read_code_note))
    return Page(state, content=content_list)

@route
def change_phaser_mode(state:State)->Page:
    return Page(state, content=[
        Header('Phaser Setting Selection'),
        'Select your new Phaser Setting.',
        SelectBox('new_phaser_mode', ['Standard', 'Stun', 'Kill'], state.phaser_setting),
        LineBreak(),
        ' ',
        Button('Confirm New Phaser Mode', change_phaser_mode_action),
        Button('Back to Pockets', pockets)
    ])

@route
def change_phaser_mode_action(state:State, new_phaser_mode:str)->Page:
    if new_phaser_mode == state.phaser_setting:
        return change_phaser_mode(state)
    elif new_phaser_mode != state.phaser_setting:
        if new_phaser_mode == 'Standard':
            if state.phaser_setting == 'Stun':
                state.player_max_damage += 6
            elif state.phaser_setting == 'Kill':
                state.player_max_damage -= 8
            state.phaser_setting = 'Standard'
            return change_phaser_mode(state)
        elif new_phaser_mode == 'Stun':
            if state.phaser_setting == 'Kill':
                state.player_max_damage -= 8
            state.phaser_setting = 'Stun'
            state.player_max_damage -= 6
            return change_phaser_mode(state)
        elif new_phaser_mode == 'Kill':
            if state.phaser_setting == 'Stun':
                state.player_max_damage += 6
            state.phaser_setting = 'Kill'
            state.player_max_damage += 8
            return change_phaser_mode(state)

@route
def use_life_boost(state:State)->Page:
    state.pockets.remove('Life Boost')
    state.player_max_health += 2
    state.player_current_health += 2
    return pockets(state)

@route
def use_strength_boost(state:State)->Page:
    state.pockets.remove('Strength Boost')
    state.player_max_damage += 2
    return pockets(state)

@route
def equipping_items(state:State)->Page:
    possible_armor = ['Starfleet Uniform']
    if 'Light Vest' in state.pockets or state.equipped_armor == 'Light Vest':
        possible_armor.append('Light Vest')
    if 'Reinforced Vest' in state.pockets or state.equipped_armor == 'Reinforced Vest':
        possible_armor.append('Reinforced Vest')
    possible_weapons = ['Hands']
    if state.user_role == 'Engineer ':
        if state.equipped_weapon == 'Basic Phaser':
            possible_weapons = ['Basic Phaser']
    elif state.user_role != 'Engineer ':
        if 'Basic Phaser' in state.pockets or state.equipped_weapon == 'Basic Phaser':
            possible_weapons.append('Basic Phaser')
        if 'Torch' in state.pockets or state.equipped_weapon == 'Torch':
            possible_weapons.append('Torch')
        if 'Crowbar' in state.pockets or state.equipped_weapon == 'Crowbar':
            possible_weapons.append('Crowbar')
    return Page(state, content=[
        Header('Item Selection'),
        'Select your Armor:',
        SelectBox('new_armor_choice', possible_armor, state.equipped_armor),
        LineBreak(),
        'Select your Weapon',
        SelectBox('new_weapon_choice', possible_weapons, state.equipped_weapon),
        LineBreak(),
        ' ',
        Button('Equip Items', equipping_items_action),
        Button('Back to Pockets', pockets)
    ])

@route
def equipping_items_action(state:State, new_armor_choice:str, new_weapon_choice:str)->Page:
    if new_armor_choice == state.equipped_armor:
        state.equipped_armor = new_armor_choice
    elif new_armor_choice != state.equipped_armor:
        if new_armor_choice == 'Starfleet Uniform':
            if state.equipped_armor == 'Light Vest':
                state.pockets.append('Light Vest')
                state.player_armor -= 1
            elif state.equipped_armor == 'Reinforced Vest':
                state.pockets.append('Reinforced Vest')
                state.player_armor -= 2
            state.equipped_armor = 'Starfleet Uniform'
        elif new_armor_choice == 'Light Vest':
            if state.equipped_armor == 'Starfleet Uniform':
                state.pockets.remove('Light Vest')
            elif state.equipped_armor == 'Reinforced Vest':
                state.pockets.remove('Light Vest')
                state.pockets.append('Reinforced Vest')
                state.player_armor -= 2
            state.equipped_armor = 'Light Vest'
            state.player_armor += 1
        elif new_armor_choice == 'Reinforced Vest':
            if state.equipped_armor == 'Starfleet Uniform':
                state.pockets.remove('Reinforced Vest')
            elif state.equipped_armor == 'Light Vest':
                state.pockets.remove('Reinforced Vest')
                state.pockets.append('Light Vest')
                state.player_armor -= 1
            state.equipped_armor = 'Reinforced Vest'
            state.player_armor += 2
    if new_weapon_choice == state.equipped_weapon:
        state.equipped_weapon = new_weapon_choice
    elif new_weapon_choice != state.equipped_weapon:
        if new_weapon_choice == 'Hands':
            if state.equipped_weapon == 'Basic Phaser':
                state.player_max_damage -= 2
                state.pockets.append('Basic Phaser')
            elif state.equipped_weapon == 'Torch':
                state.player_max_damage += 2
                state.pockets.append('Torch')
            elif state.equipped_weapon == 'Crowbar':
                state.pockets.append('Crowbar')
            state.equipped_weapon = 'Hands'
        elif new_weapon_choice == 'Basic Phaser':
            if state.equipped_weapon == 'Hands':
                state.pockets.remove('Basic Phaser')
            elif state.equipped_weapon == 'Torch':
                state.player_max_damage += 2
                state.pockets.append('Torch')
                state.pockets.remove('Basic Phaser')
            elif state.equipped_weapon == 'Crowbar':
                state.pockets.append('Crowbar')
                state.pockets.remove('Basic Phaser')
            state.equipped_weapon = 'Basic Phaser'
            state.player_max_damage += 2
        elif new_weapon_choice == 'Torch':
            if state.equipped_weapon == 'Hands':
                state.pockets.remove('Torch')
            elif state.equipped_weapon == 'Basic Phaser':
                state.player_max_damage -= 2
                state.pockets.append('Basic Phaser')
                state.pockets.remove('Torch')
            elif state.equipped_weapon == 'Crowbar':
                state.pockets.append('Crowbar')
                state.pockets.remove('Torch')
            state.equipped_weapon = 'Torch'
            state.player_max_damage -= 2
        elif new_weapon_choice == 'Crowbar':
            if state.equipped_weapon == 'Hands':
                state.pockets.remove('Crowbar')
            elif state.equipped_weapon == 'Basic Phaser':
                state.player_max_damage -= 2
                state.pockets.append('Basic Phaser')
                state.pockets.remove('Crowbar')
            elif state.equipped_weapon == 'Torch':
                state.player_max_damage += 2
                state.pockets.append('Torch')
                state.pockets.remove('Crowbar')
            state.equipped_weapon = 'Crowbar'
    if state.player_max_damage <= 0:
        return loss_damage(state)
    else:
        return equipping_items(state)

@route
def read_code_note(state:State)->Page:
    return Page(state, content=[
        Header('Terminal Code Note'),
        'The Code is ' + state.starfleet_code,
        LineBreak(),
        ' ',
        Button('Finish Reading Note', pockets)
    ])   
        
def drink_roll()->int:
    rolled_value = randint(1,100)
    return rolled_value

#Game Priming/Pockets^ -------------------------------------- Win/Loss Screens ⌄ -----------------------------------

@route
def loss_damage(state:State)->Page:
    return Page(state, content=[
        Header('Death'),
        'You became unable to deal any damage. As such, you were easily overrun and defeated.',
        LineBreak(),
        ' ',
        Button('Try Again?', game_restart)
    ])

@route
def drinking_loss_health(state:State)->Page:
    return Page(state, content=[
        Header('Death'),
        'You lost all of your health and promptly perished.',
        LineBreak(),
        ' ',
        Button('Try Again?', game_restart)
    ])

@route
def combat_loss(state:State)->Page:
    return Page(state, content=[
        Header('Death'),
        'You fought nobly, but ultimately succumbed to the might of the enemy.',
        LineBreak(),
        ' ',
        Button('Try Again?', game_restart)
    ])

@route
def game_restart(state:State)->Page:
    return index(initial_state)

@route
def game_win(state:State)->Page:
    return Page(state, content=[
        Header('Victory'),
        'You successfully fixed the ship and cleared all enemies! Congratulations!',
        LineBreak(),
        ' ',
        Button('Play Again?', game_restart)
    ])

#Win/Loss Screens ^ ---------------------------------------Initial Selections/More Priming ⌄ ------------------------

@route
def name_change(state:State, rename:str)->Page:
    rename = rename.strip()
    state.user_name = rename
    state.message = 'Now, pick your role aboard the ship.'
    return Role_Select(state)

@route
def Role_Select(state:State)->Page:
    return Page(state, content=[
        Header('Star Trek Repair Character Choice'),
        state.message,
        Button('Engineer', Engineer_Role),
        Button('Science Officer', Science_Role),
        Button('Medical Officer', Medical_Role),
        Button('Security Officer', Security_Role)
    ])

@route
def Engineer_Role(state:State)->Page:
    state.user_role = 'Engineer '
    return Page(state, content=[
        'This role will allow you to modify certain tools.',
        LineBreak(),
        'Max Health: 30',
        'Max Damage: 10',
        LineBreak(),
        'Would you like to confirm your role as Engineer?',
        Button('Confirm Role', role_confirm),
        Button('Select Different Role', Role_Select)
    ])

@route
def Science_Role(state:State)->Page:
    state.user_role = 'Scientist '
    return Page(state, content=[
        'This role will allow you to make certain crafts in the Lab.',
        LineBreak(),
        'Max Health: 25',
        'Max Damage: 8',
        LineBreak(),
        'Would you like to confirm your role as Science Officer?',
        Button('Confirm Role', role_confirm),
        Button('Select Different Role', Role_Select)
    ])

@route
def Medical_Role(state:State)->Page:
    state.user_role = 'Doctor '
    return Page(state, content=[
        'This role will allow you to heal yourself more.',
        LineBreak(),
        'Max Health: 25',
        'Max Damage: 10',
        LineBreak(),
        'Would you like to confirm your role as Medical Officer?',
        Button('Confirm Role', role_confirm),
        Button('Select Different Role', Role_Select)
    ])

@route
def Security_Role(state:State)->Page:
    state.user_role = 'Security Commander '
    return Page(state, content=[
        'This role will allow you to view security cameras.',
        LineBreak(),
        'Max Health: 35',
        'Max Damage: 12',
        LineBreak(),
        'Would you like to confirm your role as Security Officer?',
        Button('Confirm Role', role_confirm),
        Button('Select Different Role', Role_Select)
    ])

@route
def role_confirm(state:State)->Page:
    state.user_full_name = state.user_role + state.user_name
    return player_set_up(state)

@route
def player_set_up(state:State)->Page:
    if state.user_role == 'Engineer ':
        state.player_current_health = 30
        state.player_max_health = 30
        state.player_max_damage = 10
    elif state.user_role == 'Scientist ':
        state.player_current_health = 25
        state.player_max_health = 25
        state.player_max_damage = 8
    elif state.user_role == 'Doctor ':
        state.player_current_health = 25
        state.player_max_health = 25
        state.player_max_damage = 10
    elif state.user_role == 'Security Commander ':
        state.player_current_health = 35
        state.player_max_health = 35
        state.player_max_damage = 12
    return Elevator(state)

@route
def player_card(state:State)->Page:
    max_damage = 'Current Maximum Damage: ' + str(state.player_max_damage)
    health_display = 'Current Health: ' + str(state.player_current_health) + ' / ' + str(state.player_max_health)
    armor_display = 'Current Armor: ' + str(state.player_armor)
    damage_buff_display = 'Current Damage Buff: ' + str(state.player_damage_buff)
    objective_display = 'Current Objectives Complete: ' + str(state.total_objectives_complete) + ' / 5'
    enemy_display = 'Current Enemies Defeated: ' + str(state.total_enemies_defeated) + ' / 5'
    current_armor = 'Current Armor: ' + state.equipped_armor
    current_weapon = 'Current Weapon: ' + state.equipped_weapon
    current_phaser_setting = 'Current Phaser Setting: ' + state.phaser_setting
    content_list = [Header(state.user_full_name + "'s Player Card"),
        health_display,
        armor_display,
        max_damage,
        damage_buff_display,
        objective_display,
        enemy_display,
        current_armor,
        current_weapon,
    ]
    if state.user_role == 'Engineer ':
        if 'Basic Phaser' in state.pockets:
            content_list.append(current_phaser_setting)
    content_list.append(LineBreak())
    content_list.append(' ')
    content_list.append(float_right(Button('Check Pockets', pockets, margin_right=87)))
    content_list.append(float_right(Button('Close Player Card', state.last_location, margin_right=5)))
    return Page(state, content=[
        Header(state.user_full_name + "'s Player Card"),
        health_display,
        armor_display,
        max_damage,
        damage_buff_display,
        objective_display,
        enemy_display,
        current_armor,
        current_weapon,
        LineBreak(),
        ' ',
        float_right(Button('Check Pockets', pockets, margin_right=87)),
        float_right(Button('Close Player Card', state.last_location, margin_right=5)),
    ])

#Initial Selections/More Priming ^ --------------------- Elevator ⌄ --------------------------------------------------------

@route
def Elevator(state:State)->Page:
    state.last_location = 'Elevator'
    return Page(state, content=[
        Header('Elevator'),
        'Which level would you like to go to?',
        Button('Command Level', Command_Level),
        Button('Operations Level', Operations_Level),
        Button('Science Level', Science_Level),
        Button('Crew Level', Crew_Level),
        Button('Security Level', Security_Level),
        LineBreak(),
        ' ',
        float_right(Button('Check Pockets', pockets, margin_right=87)),
        float_right(Button('View Player Card', player_card, margin_right=5)),
        Button('Search Elevator', elevator_search),
    ])

@route
def elevator_search(state:State)->Page:
    state.last_location = 'elevator_search'
    if not state.elevator_searched:
        state.pockets.append('Tool Box')
        state.elevator_searched = True
        return Page(state, content=[
            Header('Elevator'),
            'You found a Tool Box!',
            LineBreak(),
            ' ',
            Button('Finish Searching', Elevator),
            float_right(Button('Check Pockets', pockets, margin_right=87)),
            float_right(Button('View Player Card', player_card, margin_right=5)),
        ])
    elif state.elevator_searched:
        return Page(state, content=[
            Header('Elevator'),
            'There is nothing left to find in the Elevator.',
            LineBreak(),
            ' ',
            Button('Finish Searching', Elevator),
            float_right(Button('Check Pockets', pockets, margin_right=87)),
            float_right(Button('View Player Card', player_card, margin_right=5)),
        ])

#Elevator ^ -------------------------------- Command Level ⌄ --------------------------------------------------

@route
def Command_Level(state:State)->Page:
    state.last_location = 'Command_Level'
    return Page(state, content=[
        Header('Command Level'),
        'Where on the Command Level would you like to go?',
        Button('The Bridge', Bridge),
        Button('Observation Lounge', Observation_Lounge),
        Button("Captain's Office", Captains_Office),
        LineBreak(),
        ' ',
        float_right(Button('Check Pockets', pockets, margin_right=87)),
        float_right(Button('View Player Card', player_card, margin_right=5)),
        Button('Back to Elevator', Elevator)
    ])

@route
def Bridge(state:State)->Page:
    state.last_location = 'Bridge'
    return Page(state, content=[
        Header('Bridge'),
        'What would you like to do on the Bridge?',
        Button('Examine Terminal', terminal),
        LineBreak(),
        ' ',
        float_right(Button('Check Pockets', pockets)),
        float_right(Button('View Player Card', player_card, margin_right=5)),
        Button('Return to Command Level', Command_Level)
    ])

@route
def terminal (state:State)->Page:
    state.last_location = 'terminal'
    if (('Terminal Electronic Component' in state.pockets and 'Tool Box' in state.pockets) or state.fixed_terminal):
        if 'Terminal Electronic Component' in state.pockets:
            state.pockets.remove('Terminal Electronic Component')
            state.fixed_terminal = True
            state.total_objectives_complete += 1
            state.message = 'You fixed the Terminal! What would you like to do in the Terminal?'
        elif 'Terminal Electronic Component' not in state.pockets:
            state.message = 'What would you like to do in the Terminal?'
        return Page(state, content=[
            Header('Terminal'),
            state.message,
            Button('Input Starfleet Code',starfleet_code),
            Button('View Security Cameras', security_cameras),
            LineBreak(),
            ' ',
            float_right(Button('Check Pockets', pockets, margin_right=87)),
            float_right(Button('View Player Card', player_card, margin_right=5)),
            Button('Exit Terminal', Bridge)
        ])
    elif 'Terminal Electronic Component' not in state.pockets and 'Tool Box' in state.pockets:
        return Page(state, content=[
            Header('Terminal'),
            'The Terminal seems to be missing a component in order to work.',
            Button('Exit Terminal', Bridge),
            float_right(Button('Check Pockets', pockets, margin_right=87)),
            float_right(Button('View Player Card', player_card, margin_right=5)),
        ])
    elif 'Terminal Electronic Component' in state.pockets and 'Tool Box' not in state.pockets:
        return Page(state, content=[
            Header('Terminal'),
            'You seem to be missing the correct tools in order to fix the Terminal.',
            Button('Exit Terminal', Bridge),
            float_right(Button('Check Pockets', pockets, margin_right=87)),
            float_right(Button('View Player Card', player_card, margin_right=5)),
        ])
    elif ('Terminal Electronic Component' and 'Tool Box') not in state.pockets:
        return Page(state, content=[
            Header('Terminal'),
            'You seem to be missing the correct tools and a certain component in order to fix the Terminal.',
            Button('Exit Terminal', Bridge),
            float_right(Button('Check Pockets', pockets, margin_right=87)),
            float_right(Button('View Player Card', player_card, margin_right=5)),
        ])
    
@route
def security_cameras(state:State)->Page:
    if state.user_role == 'Security Commander ':    
        return Page(state, content=[
            Header('Security Cameras'),
            'Which Level would you like to view?',
            Button('Command Level', command_level_cameras),
            Button('Operations Level', operations_level_cameras),
            Button('Science Level', science_level_cameras),
            Button('Crew Level', crew_level_cameras),
            Button('Security Level', security_level_cameras),
            LineBreak(),
            ' ',
            float_right(Button('Check Pockets', pockets, margin_right=87)),
            float_right(Button('View Player Card', player_card, margin_right=5)),
            Button('Exit Security Cameras', terminal),
        ])
    elif state.user_role != "Security Commander ":
        return Page(state, content=[
            Header('Security Cameras'),
            'You do not have access to view the Security Cameras',
            LineBreak(),
            ' ',
            float_right(Button('Check Pockets', pockets, margin_right=87)),
            float_right(Button('View Player Card', player_card, margin_right=5)),
            Button('Exit Security Cameras', terminal),
        ])

@route
def command_level_cameras(state:State)->Page:
    state.last_location = 'command_level_cameras'
    return Page(state, content=[
        Header('Security Cameras'),
        'There are 0 enemies on the Bridge.',
        'There are 0 enemies in the Observation Lounge.',
        "There is 1 enemy in the Captain's Office.",
        LineBreak(),
        ' ',
        float_right(Button('Check Pockets', pockets, margin_right=87)),
        float_right(Button('View Player Card', player_card, margin_right=5)),
        Button('Exit Command Level Security Cameras', security_cameras),
    ])
        

@route
def operations_level_cameras(state:State)->Page:
    state.last_location = 'operations_level_cameras'
    return Page(state, content=[
        Header('Security Cameras'),
        'There are 0 enemies in Main Engineering.',
        'There is 1 enemy in the Transporter Room.',
        "There are 0 enemies in Cargo Bay.",
        LineBreak(),
        ' ',
        float_right(Button('Check Pockets', pockets, margin_right=87)),
        float_right(Button('View Player Card', player_card, margin_right=5)),
        Button('Exit Operations Level Security Cameras', security_cameras),
    ])

@route
def science_level_cameras(state:State)->Page:
    state.last_location = 'science_level_cameras'
    return Page(state, content=[
        Header('Security Cameras'),
        'There are 0 enemies in Sick Bay.',
        'There are 0 enemies in Storage.',
        "There are 0 enemies in the Lab.",
        LineBreak(),
        ' ',
        float_right(Button('Check Pockets', pockets, margin_right=87)),
        float_right(Button('View Player Card', player_card, margin_right=5)),
        Button('Exit Science Level Security Cameras', security_cameras),
    ])

@route
def crew_level_cameras(state:State)->Page:
    state.last_location = 'crew_level_cameras'
    return Page(state, content=[
        Header('Security Cameras'),
        'There is 1 enemy in the Mess Hall.',
        'There are 0 enemies in Quarter 1.',
        'There are 0 enemies in Quarter 2.',
        'There is 1 enemy in Quarter 3.',
        "There are 0 enemies at the Bar.",
        LineBreak(),
        ' ',
        float_right(Button('Check Pockets', pockets, margin_right=87)),
        float_right(Button('View Player Card', player_card, margin_right=5)),
        Button('Exit Crew Level Security Cameras', security_cameras),
    ])

@route
def security_level_cameras(state:State)->Page:
    state.last_location = 'security_level_cameras'
    return Page(state, content=[
        Header('Security Cameras'),
        'There are 0 enemies in the Armory.',
        "There is 1 enemy in the Jail.",
        LineBreak(),
        ' ',
        float_right(Button('Check Pockets', pockets, margin_right=87)),
        float_right(Button('View Player Card', player_card, margin_right=5)),
        Button('Exit Security Level Security Cameras', security_cameras),
    ])

@route
def starfleet_code(state:State)->Page:
    state.last_location = 'starfleet_code'
    if state.total_objectives_complete == 4 and state.total_enemies_defeated == 5:
        return Page(state, content=[
            Header('Terminal'),
            'Enter the code to Starfleet to confirm safety:',
            TextBox('code_input'),
            Button('Send Code', code_send),
            LineBreak(),
            ' ',
            float_right(Button('Check Pockets', pockets, margin_right=87)),
            float_right(Button('View Player Card', player_card, margin_right=5)),
            Button('Exit Code Input', terminal),
        ])
    elif state.total_objectives_complete != 4 or state.total_enemies_defeated != 5:
        return Page(state, content=[
            Header('Terminal'),
            'It would be unwise to tell Starfleet you are okay while not everything is done.',
            LineBreak(),
            ' ',
            float_right(Button('Check Pockets', pockets, margin_right=87)),
            float_right(Button('View Player Card', player_card, margin_right=5)),
            Button('Exit Code Input', terminal),
        ])

@route
def code_send(state:State, code_input:str)->Page:
    state.last_location = 'code_send'
    if code_input == state.starfleet_code:
        return game_win(state)
    elif code_input != state.starfleet_code:
        return Page(state, content=[
            Header('Terminal'),
            'That code was incorrect. Please try again.',
            TextBox('user_input_code'),
            Button('Send Code', code_send),
            LineBreak(),
            ' ',
            float_right(Button('Check Pockets', pockets, margin_right=87)),
            float_right(Button('View Player Card', player_card, margin_right=5)),
            Button('Exit Code Input', terminal),
        ])

@route
def Observation_Lounge(state:State)->Page:
    state.last_location = 'Observation_Lounge'
    return Page(state, content=[
        Header('Observation Lounge'),
        'What would you like to do on the Observation Lounge?',
        Button('Look Into Space', space_gander),
        Button('Search Lounge', lounge_search),
        LineBreak(),
        ' ',
        float_right(Button('Check Pockets', pockets, margin_right=87)),
        float_right(Button('View Player Card', player_card, margin_right=5)),
        Button('Exit Observation Lounge', Command_Level)
    ])

@route
def space_gander(state:State)->Page:
    state.last_location = 'space_gander'
    return Page(state, content=[
        Header('Observation Lounge'),
        'You looked into space (pretend there is an image here)',
        LineBreak(),
        ' ',
        Button('Stop Looking Into Space', Observation_Lounge),
        float_right(Button('Check Pockets', pockets, margin_right=87)),
        float_right(Button('View Player Card', player_card, margin_right=5)),
    ])

@route
def lounge_search(state:State)->Page:
    state.last_location = 'lounge_search'
    if not state.lounge_searched:
        state.pockets.append('Key Card')
        state.lounge_searched = True
        return Page(state, content=[
            Header('Observation Lounge'),
            'You found a Key Card!',
            LineBreak(),
            ' ',
            Button('Finish Searching', Observation_Lounge),
            float_right(Button('Check Pockets', pockets, margin_right=87)),
            float_right(Button('View Player Card', player_card, margin_right=5)),
        ])
    elif state.lounge_searched:
        return Page(state, content=[
            Header('Observation Lounge'),
            'There is nothing left to find in the Observation Lounge.',
            LineBreak(),
            ' ',
            Button('Finish Searching', Observation_Lounge),
            float_right(Button('Check Pockets', pockets, margin_right=87)),
            float_right(Button('View Player Card', player_card, margin_right=5)),
        ])
    
@route
def Captains_Office(state:State)->Page:
    state.last_location = 'Captains_Office'
    if not state.enemy_1_defeated:
        return Page(state, content=[
            Header("Captain's Office - ALERT"),
            "A hostile boarder is ransacking the office! You have no choice but to fight.",
            LineBreak(),
            Button('Engage in Combat', setup_combat_1)
        ])
    elif state.enemy_1_defeated:
        return Page(state, content=[
            Header("Captain's Office"),
            'The enemy lies defeated on the floor. The room is clear.',
            LineBreak(),
            ' ',
            float_right(Button('Check Pockets', pockets, margin_right=87)),
            float_right(Button('View Player Card', player_card, margin_right=5)),
            Button('Exit Office', Command_Level)
        ])

@route
def setup_combat_1(state:State)->Page:
    state.current_enemy = 1
    state.current_burn_value = 0
    return combat_loop(state)

#Command Level ^ -------------------------------- Operations Level ⌄ --------------------------------------------------

@route
def Operations_Level(state:State)->Page:
    state.last_location = 'Operations_Level'
    return Page(state, content=[
        Header('Operations Level'),
        'Where on the Operations Level would you like to go?',
        Button('Main Engineering', Main_Engineering),
        Button('Transporter Room', Transporter_Room),
        Button("Cargo Bay", Cargo_Bay),
        LineBreak(),
        ' ',
        float_right(Button('Check Pockets', pockets, margin_right=87)),
        float_right(Button('View Player Card', player_card, margin_right=5)),
        Button('Back to Elevator', Elevator)
    ])

@route
def Main_Engineering(state:State)->Page:
    state.last_location = 'Main_Engineering'
    if 'Key Card' not in state.pockets:
        return Page(state, content=[
            Header('Main Engineering'),
            'You need a Key Card to access Main Engineering',
            LineBreak(),
            ' ',
            float_right(Button('Check Pockets', pockets, margin_right=87)),
            float_right(Button('View Player Card', player_card, margin_right=5)),
            Button('Exit Main Engineering', Operations_Level)
        ])
    elif 'Key Card' in state.pockets:
        if not ('Spare Glass' in state.pockets or state.fixed_reactor_core):
            return Page(state, content=[
                Header('Main Engineering'),
                'The Warp Core glass is broken, it needs to be fixed!',
                LineBreak(),
                ' ',
                float_right(Button('Check Pockets', pockets, margin_right=87)),
                float_right(Button('View Player Card', player_card, margin_right=5)),
                Button('Exit Main Engineering', Operations_Level)
            ])
        elif 'Spare Glass' in state.pockets or state.fixed_reactor_core:
            if 'Spare Glass' in state.pockets:
                state.pockets.remove('Spare Glass')
                state.fixed_reactor_core = True
                state.total_objectives_complete += 1
                return Page(state, content=[
                    Header('Main Engineering'),
                    'You fixed the Warp Core!',
                    Button('Search Main Engineering', engineering_search),
                    LineBreak(),
                    ' ',
                    float_right(Button('Check Pockets', pockets, margin_right=87)),
                    float_right(Button('View Player Card', player_card, margin_right=5)),
                    Button('Exit Main Engineering', Operations_Level),
                ])
            elif state.fixed_reactor_core:
                return Page(state, content=[
                    Header('Main Engineering'),
                    'What would you like to do in Main Engineering?',
                    Button('Search Main Engineering', engineering_search),
                    LineBreak(),
                    ' ',
                    float_right(Button('Check Pockets', pockets, margin_right=87)),
                    float_right(Button('View Player Card', player_card, margin_right=5)),
                    Button('Exit Main Engineering', Operations_Level),
                ])

@route
def engineering_search(state:State)->Page:
    state.last_location = 'engineering_search'
    if not state.engineering_searched:
        state.pockets.append('Terminal Electronic Component')
        state.engineering_searched = True
        return Page(state, content=[
            Header('Main Engineering'),
            'You found the Terminal Electronic Component!',
            LineBreak(),
            ' ',
            Button('Finish Searching', Main_Engineering),
            float_right(Button('Check Pockets', pockets, margin_right=87)),
            float_right(Button('View Player Card', player_card, margin_right=5)),
        ])
    elif state.engineering_searched:
        return Page(state, content=[
            Header('Main Engineering'),
            'There is nothing left to find in Main Engineering.',
            LineBreak(),
            ' ',
            Button('Finish Searching', Main_Engineering),
            float_right(Button('Check Pockets', pockets, margin_right=87)),
            float_right(Button('View Player Card', player_card, margin_right=5)),
        ])
                    
@route
def Transporter_Room(state:State)->Page:
    state.last_location = 'Transporter_Room'
    if not state.enemy_2_defeated:
        return Page(state, content=[
            Header("Transporter Room - ALERT"),
            "An enemy has beamed in and is attempting to lock out the console! You must fight.",
            LineBreak(),
            Button('Engage in Combat', setup_combat_2)
        ])
    elif state.enemy_2_defeated:
        return Page(state, content=[
            Header("Transporter Room"),
            'The enemy is defeated. The transporter pads are quiet.',
            Button('Use Transporter', use_transporter),
            LineBreak(),
            ' ',
            float_right(Button('Check Pockets', pockets, margin_right=87)),
            float_right(Button('View Player Card', player_card, margin_right=5)),
            Button('Exit Transporter Room', Operations_Level)
        ])
    
@route
def use_transporter(state:State)->Page:
    state.last_location = 'use_transporter'
    if not state.transporter_used:
        state.transporter_used = True
        state.pockets.append('Scrap Metal')
        return Page(state, content=[
            Header('Transporter'),
            'The Transporter brought you a piece of Scrap Metal!',
            LineBreak(),
            ' ',
            Button('Finish Transporting', Transporter_Room),
            float_right(Button('Check Pockets', pockets, margin_right=87)),
            float_right(Button('View Player Card', player_card, margin_right=5)),
        ])
    elif state.transporter_used:
        return Page(state, content=[
            Header('Transporter'),
            'There is nothing left for the Transporter to bring you!',
            LineBreak(),
            ' ',
            Button('Finish Transporting', Transporter_Room),
            float_right(Button('Check Pockets', pockets, margin_right=87)),
            float_right(Button('View Player Card', player_card, margin_right=5)),
        ])

@route
def setup_combat_2(state:State)->Page:
    state.current_enemy = 2
    state.current_burn_value = 0
    return combat_loop(state)
    

@route
def Cargo_Bay(state:State)->Page:
    state.last_location = 'Cargo_Bay'
    return Page(state, content=[
        Header('Cargo Bay'),
        'What would you like to do in the Cargo Bay?',
        Button('Search Cargo Bay', cargo_search),
        LineBreak(),
        ' ',
        float_right(Button('Check Pockets', pockets, margin_right=87)),
        float_right(Button('View Player Card', player_card, margin_right=5)),
        Button('Exit Cargo Bay', Operations_Level),
    ])

@route
def cargo_search(state:State)->Page:
    state.last_location = 'cargo_search'
    return Page(state, content=[
        Header('Cargo Bay'),
        'You search Cargo Bay and find some crates. Would you like to search them?',
        Button('Search Crate 1', crate1_search),
        Button('Search Crate 2', crate2_search),
        Button('Search Crate 3', crate3_search),
        Button('Search Crate 4', crate4_search),
        LineBreak(),
        ' ',
        Button('Finish Searching', Cargo_Bay),
        float_right(Button('Check Pockets', pockets, margin_right=87)),
        float_right(Button('View Player Card', player_card, margin_right=5)),
    ])

@route
def crate1_search(state:State)->Page:
    state.last_location = 'crate1_search'
    return Page(state, content=[
        Header('Crate 1'),
        'There is nothing in Crate 1',
        LineBreak(),
        ' ',
        Button('Finish Searching', cargo_search),
        float_right(Button('Check Pockets', pockets, margin_right=87)),
        float_right(Button('View Player Card', player_card, margin_right=5)),
    ])

@route
def crate2_search(state:State)->Page:
    state.last_location = 'crate2_search'
    if not state.crate2_searched:
        state.crate2_searched = True
        state.pockets.append('Spare Hinges')
        return Page(state, content=[
            Header('Crate 2'),
            'You found some Spare Hinges!',
            LineBreak(),
            ' ',
            Button('Finish Searching', cargo_search),
            float_right(Button('Check Pockets', pockets, margin_right=87)),
            float_right(Button('View Player Card', player_card, margin_right=5)),
        ])
    elif state.crate2_searched:
        return Page(state, content=[
            Header('Crate 2'),
            'There is nothing else in Crate 2',
            LineBreak(),
            ' ',
            Button('Finish Searching', cargo_search),
            float_right(Button('Check Pockets', pockets, margin_right=87)),
            float_right(Button('View Player Card', player_card, margin_right=5)),
        ])

@route
def crate3_search(state:State)->Page:
    state.last_location = 'crate3_search'
    if not state.crate3_searched:
        state.crate3_searched = True
        state.pockets.append('Piping')
        return Page(state, content=[
            Header('Crate 3'),
            'You found some Piping!',
            LineBreak(),
            ' ',
            Button('Finish Searching', cargo_search),
            float_right(Button('Check Pockets', pockets, margin_right=87)),
            float_right(Button('View Player Card', player_card, margin_right=5)),
        ])
    elif state.crate3_searched:
        return Page(state, content=[
            Header('Crate 3'),
            'There is nothing else in Crate 3',
            LineBreak(),
            ' ',
            Button('Finish Searching', cargo_search),
            float_right(Button('Check Pockets', pockets, margin_right=87)),
            float_right(Button('View Player Card', player_card, margin_right=5)),
        ])
@route
def crate4_search(state:State)->Page:
    state.last_location = 'crate4_search'
    return Page(state, content=[
        Header('Crate 4'),
        'There is nothing in Crate 4',
        LineBreak(),
        ' ',
        Button('Finish Searching', cargo_search),
        float_right(Button('Check Pockets', pockets, margin_right=87)),
        float_right(Button('View Player Card', player_card, margin_right=5)),
    ])

#Operations Level ^ -------------------------------- Science Level ⌄ --------------------------------------------------

@route
def Science_Level(state:State)->Page:
    state.last_location = 'Science_Level'
    return Page(state, content=[
        Header('Science Level'),
        'Where on the Science Level would you like to go?',
        Button('Sick Bay', Sick_Bay),
        Button('Storage', Storage),
        Button("Science Lab", Science_Lab),
        LineBreak(),
        ' ',
        float_right(Button('Check Pockets', pockets, margin_right=87)),
        float_right(Button('View Player Card', player_card, margin_right=5)),
        Button('Back to Elevator', Elevator)
    ])

@route
def Sick_Bay(state:State)->Page:
    state.last_location = 'Sick_Bay'
    return Page(state, content=[
        Header('Sick Bay'),
        'What would you like to do in Sick Bay?',
        Button('Use Medical Table', medical_table),
        LineBreak(),
        ' ',
        Button('Leave Sick Bay', Science_Level),
        float_right(Button('Check Pockets', pockets, margin_right=87)),
        float_right(Button('View Player Card', player_card, margin_right=5)),
    ])

@route
def medical_table(state:State)->Page:
    state.last_location = 'medical_table'
    if state.player_current_health == state.player_max_health:
        return Page(state, content=[
                Header('Medical Table'),
                'You are at Maximum Health! It would be a waste to use the Medical Table now.',
                LineBreak(),
                ' ',
                Button('Leave Medical Table', Sick_Bay),
                float_right(Button('Check Pockets', pockets, margin_right=87)),
                float_right(Button('View Player Card', player_card, margin_right=5)),
            ])
    elif state.user_role == 'Doctor ':
        state.player_current_health = state.player_max_health
        return Page(state, content=[
            Header('Medical Table'),
            'You were healed up to your maximum health!',
            LineBreak(),
            ' ',
            Button('Leave Medical Table', Sick_Bay),
            float_right(Button('Check Pockets', pockets, margin_right=87)),
            float_right(Button('View Player Card', player_card, margin_right=5)),
        ])
    elif state.user_role != 'Doctor ':
        if state.remaining_heals > 0:
            state.remaining_heals -= 1
            state.player_current_health = state.player_max_health
            return Page(state, content=[
                Header('Medical Table'),
                'You were healed up to your maximum health!',
                'You can use the Medical Table ' + str(state.remaining_heals) + ' times.',
                LineBreak(),
                ' ',
                Button('Leave Medical Table', Sick_Bay),
                float_right(Button('Check Pockets', pockets, margin_right=87)),
                float_right(Button('View Player Card', player_card, margin_right=5)),
            ])
        elif state.remaining_heals == 0:
            return Page(state, content=[
                Header('Medical Table'),
                'The Medical Table is out of energy and can no longer be used.',
                LineBreak(),
                ' ',
                Button('Leave Medical Table', Sick_Bay),
                float_right(Button('Check Pockets', pockets, margin_right=87)),
                float_right(Button('View Player Card', player_card, margin_right=5)),
            ])

@route
def Storage(state:State)->Page:
    state.last_location = 'Storage'
    return Page(state, content=[
        Header('Storage'),
        'What would you like to do in Storage?',
        Button('Search Storage', storage_search),
        LineBreak(),
        ' ',
        float_right(Button('Check Pockets', pockets, margin_right=87)),
        float_right(Button('View Player Card', player_card, margin_right=5)),
        Button('Exit Storage', Science_Level),
    ])

@route
def storage_search(state:State)->Page:
    state.last_location = 'storage_search'
    return Page(state, content=[
        Header('Storage'),
        'You search Storage and find some cardboard boxes. Would you like to search them?',
        Button('Search Box 1', box1_search),
        Button('Search Box 2', box2_search),
        Button('Search Box 3', box3_search),
        LineBreak(),
        ' ',
        Button('Finish Searching', Cargo_Bay),
        float_right(Button('Check Pockets', pockets, margin_right=87)),
        float_right(Button('View Player Card', player_card, margin_right=5)),
    ])

@route
def box1_search(state:State)->Page:
    state.last_location = 'box1_search'
    if not state.box1_searched:
        state.pockets.append('Empty Injector')
        state.box1_searched = True
        return Page(state, content=[
            Header('Box 1'),
            'You found an Empty Injector!',
            LineBreak(),
            ' ',
            Button('Finish Searching', storage_search),
            float_right(Button('Check Pockets', pockets, margin_right=87)),
            float_right(Button('View Player Card', player_card, margin_right=5)),
        ])
    elif state.box1_searched:
        return Page(state, content=[
            Header('Box 1'),
            'There is nothing else in Box 1',
            LineBreak(),
            ' ',
            Button('Finish Searching', storage_search),
            float_right(Button('Check Pockets', pockets, margin_right=87)),
            float_right(Button('View Player Card', player_card, margin_right=5)),
        ])

@route
def box2_search(state:State)->Page:
    state.last_location = 'box2_search'
    return Page(state, content=[
        Header('Box 2'),
        'There is nothing in Box 2',
        LineBreak(),
        ' ',
        Button('Finish Searching', storage_search),
        float_right(Button('Check Pockets', pockets, margin_right=87)),
        float_right(Button('View Player Card', player_card, margin_right=5)),
    ])

@route
def box3_search(state:State)->Page:
    state.last_location = 'box3_search'
    if not state.box3_searched:
        state.pockets.append('Inaprolavine')
        state.pockets.append('Hyperzine')
        state.box3_searched = True
        return Page(state, content=[
            Header('Box 3'),
            'You found Injector Fillings!',
            LineBreak(),
            ' ',
            Button('Finish Searching', storage_search),
            float_right(Button('Check Pockets', pockets, margin_right=87)),
            float_right(Button('View Player Card', player_card, margin_right=5)),
        ])
    elif state.box3_searched:
        return Page(state, content=[
            Header('Box 3'),
            'There is nothing else in Box 3',
            LineBreak(),
            ' ',
            Button('Finish Searching', storage_search),
            float_right(Button('Check Pockets', pockets, margin_right=87)),
            float_right(Button('View Player Card', player_card, margin_right=5)),
        ])

@route
def Science_Lab(state:State)->Page:
    state.last_location = 'Science_Lab'
    if state.user_role == 'Scientist ':
        return Page(state, content=[
            Header('Science Lab'),
            'What would you like to do in the Science Lab?',
            Button('Create Injection', make_injection),
            Button('Synthesize Object', synthesize_object),
            Button('Read Lab Manual', lab_manual),
            LineBreak(),
            ' ',
            Button('Leave Science Lab', Science_Level),
            float_right(Button('Check Pockets', pockets, margin_right=87)),
            float_right(Button('View Player Card', player_card, margin_right=5)),
        ])
    elif state.user_role != 'Scientist ':
        return Page(state, content=[
            Header('Science Lab'),
            'You do not have access to the Science Lab.',
            LineBreak(),
            ' ',
            Button('Leave Science Lab', Science_Level),
            float_right(Button('Check Pockets', pockets, margin_right=87)),
            float_right(Button('View Player Card', player_card, margin_right=5)),
        ])
    
@route
def make_injection(state:State)->Page:
    state.last_location = 'make_injection'
    return Page(state, content=[
        Header('Science Lab'),
        'Which Injection would you like to make?',
        Button('Life Boost', life_boost_injection),
        Button('Strength Boost', strength_boost_injection),
        LineBreak(),
        ' ',
        Button('Stop Making Injections', Science_Lab),
        float_right(Button('Check Pockets', pockets, margin_right=87)),
        float_right(Button('View Player Card', player_card, margin_right=5)),
    ])

@route
def life_boost_injection(state:State)->Page:
    if 'Empty Injector' in state.pockets and 'Inaprolavine' in state.pockets:
        state.pockets.remove('Empty Injector')
        state.pockets.remove('Inaprolavine')
        state.pockets.append('Life Boost')
        return Page(state, content=[
            Header('Science Lab'),
            'You made a Life Boost!',
            LineBreak(),
            ' ',
            Button('Finish Making Injection', make_injection),
            float_right(Button('Check Pockets', pockets, margin_right=87)),
            float_right(Button('View Player Card', player_card, margin_right=5)),
        ])
    elif 'Empty Injector' in state.pockets and 'Inaprolavine' not in state.pockets:
        return Page(state, content=[
            Header('Science Lab'),
            'You are missing Inaprolavine to make a Life Boost',
            LineBreak(),
            ' ',
            Button('Leave Making Injection', make_injection),
            float_right(Button('Check Pockets', pockets, margin_right=87)),
            float_right(Button('View Player Card', player_card, margin_right=5)),
        ])
    elif 'Empty Injector' not in state.pockets and 'Inaprolavine' in state.pockets:
        return Page(state, content=[
            Header('Science Lab'),
            'You are missing an Empty Injector to make a Life Boost',
            LineBreak(),
            ' ',
            Button('Leave Making Injection', make_injection),
            float_right(Button('Check Pockets', pockets, margin_right=87)),
            float_right(Button('View Player Card', player_card, margin_right=5)),
        ])
    elif 'Empty Injector' not in state.pockets and 'Inaprolavine' not in state.pockets:
        return Page(state, content=[
            Header('Science Lab'),
            'You are missing an Empty Injector and Inaprolavine to make a Life Boost',
            LineBreak(),
            ' ',
            Button('Leave Making Injection', make_injection),
            float_right(Button('Check Pockets', pockets, margin_right=87)),
            float_right(Button('View Player Card', player_card, margin_right=5)),
        ])
            
@route
def strength_boost_injection(state:State)->Page:
    if 'Empty Injector' in state.pockets and 'Hyperzine' in state.pockets:
        state.pockets.remove('Empty Injector')
        state.pockets.remove('Hyperzine')
        state.pockets.append('Strength Boost')
        return Page(state, content=[
            Header('Science Lab'),
            'You made a Strength Boost!',
            LineBreak(),
            ' ',
            Button('Finish Making Injection', make_injection),
            float_right(Button('Check Pockets', pockets, margin_right=87)),
            float_right(Button('View Player Card', player_card, margin_right=5)),
        ])
    elif 'Empty Injector' in state.pockets and 'Hyperzine' not in state.pockets:
        return Page(state, content=[
            Header('Science Lab'),
            'You are missing Hyperzine to make a Life Boost',
            LineBreak(),
            ' ',
            Button('Leave Making Injection', make_injection),
            float_right(Button('Check Pockets', pockets, margin_right=87)),
            float_right(Button('View Player Card', player_card, margin_right=5)),
        ])
    elif 'Empty Injector' not in state.pockets and 'Hyperzine' in state.pockets:
        return Page(state, content=[
            Header('Science Lab'),
            'You are missing an Empty Injector to make a Life Boost',
            LineBreak(),
            ' ',
            Button('Leave Making Injection', make_injection),
            float_right(Button('Check Pockets', pockets, margin_right=87)),
            float_right(Button('View Player Card', player_card, margin_right=5)),
        ])
    elif 'Empty Injector' not in state.pockets and 'Hyperzine' not in state.pockets:
        return Page(state, content=[
            Header('Science Lab'),
            'You are missing an Empty Injector and Hyperzine to make a Strength Boost',
            LineBreak(),
            ' ',
            Button('Leave Making Injection', make_injection),
            float_right(Button('Check Pockets', pockets, margin_right=87)),
            float_right(Button('View Player Card', player_card, margin_right=5)),
        ])

@route
def synthesize_object(state:State)->Page:
    state.last_location = 'synthesize_object'
    return Page(state, content=[
        Header('Science Lab'),
        'Which Object would you like to synthesize?',
        Button('Reinforced Vest', make_better_vest),
        Button('Torch', make_torch),
        Button('Crowbar', make_crowbar),
        LineBreak(),
        ' ',
        Button('Stop Synthesizing Objects', Science_Lab),
        float_right(Button('Check Pockets', pockets, margin_right=87)),
        float_right(Button('View Player Card', player_card, margin_right=5)),
    ])

@route
def make_better_vest(state:State)->Page:
    if 'Scrap Metal' in state.pockets and 'Fabric' in state.pockets and 'Light Vest' in state.pockets:
        state.pockets.remove('Scrap Metal')
        state.pockets.remove('Fabric')
        state.pockets.remove('Light Vest')
        state.pockets.append('Reinforced Vest')
        return Page(state, content=[
            Header('Science Lab'),
            'You made a Reinforced Vest!',
            LineBreak(),
            ' ',
            Button('Finish Synthesizing Object', synthesize_object),
            float_right(Button('Check Pockets', pockets, margin_right=87)),
            float_right(Button('View Player Card', player_card, margin_right=5)),
        ])
    elif 'Scrap Metal' in state.pockets:
        if 'Fabric' in state.pockets and 'Light Vest' not in state.pockets:
            return Page(state, content=[
                Header('Science Lab'),
                'You are missing a Light Vest in order to make a Reinforced Vest.',
                LineBreak(),
                ' ',
                Button('Leave Synthesizing Object', synthesize_object),
                float_right(Button('Check Pockets', pockets, margin_right=87)),
                float_right(Button('View Player Card', player_card, margin_right=5)),
            ])
        elif 'Fabric' not in state.pockets and 'Light Vest' in state.pockets:
            return Page(state, content=[
                Header('Science Lab'),
                'You are missing Fabric in order to make a Reinforced Vest.',
                LineBreak(),
                ' ',
                Button('Leave Synthesizing Object', synthesize_object),
                float_right(Button('Check Pockets', pockets, margin_right=87)),
                float_right(Button('View Player Card', player_card, margin_right=5)),
            ])
        elif 'Fabric' not in state.pockets and 'Light Vest' not in state.pockets:
            return Page(state, content=[
                Header('Science Lab'),
                'You are missing Fabric and a Light Vest in order to make a Reinforced Vest.',
                LineBreak(),
                ' ',
                Button('Leave Synthesizing Object', synthesize_object),
                float_right(Button('Check Pockets', pockets, margin_right=87)),
                float_right(Button('View Player Card', player_card, margin_right=5)),
            ])
    elif 'Fabric' in state.pockets:
        if 'Scrap Metal' not in state.pockets and 'Light Vest' in state.pockets:
            return Page(state, content=[
                Header('Science Lab'),
                'You are missing Scrap Metal in order to make a Reinforced Vest.',
                LineBreak(),
                ' ',
                Button('Leave Synthesizing Object', synthesize_object),
                float_right(Button('Check Pockets', pockets, margin_right=87)),
                float_right(Button('View Player Card', player_card, margin_right=5)),
            ])
        if 'Scrap Metal' not in state.pockets and 'Light Vest' not in state.pockets:
            return Page(state, content=[
                Header('Science Lab'),
                'You are missing Scrap Metal and a Light Vest in order to make a Reinforced Vest.',
                LineBreak(),
                ' ',
                Button('Leave Synthesizing Object', synthesize_object),
                float_right(Button('Check Pockets', pockets, margin_right=87)),
                float_right(Button('View Player Card', player_card, margin_right=5)),
            ])
    elif 'Scrap Metal' not in state.pockets and 'Fabric' not in state.pockets and 'Light Vest' in state.pockets:
        return Page(state, content=[
                Header('Science Lab'),
                'You are missing Scrap metal and Fabric in order to make a Reinforced Vest.',
                LineBreak(),
                ' ',
                Button('Leave Synthesizing Object', synthesize_object),
                float_right(Button('Check Pockets', pockets, margin_right=87)),
                float_right(Button('View Player Card', player_card, margin_right=5)),
            ])
    elif 'Scrap Metal' not in state.pockets and 'Fabric' not in state.pockets and 'Light Vest' not in state.pockets:
        return Page(state, content=[
                Header('Science Lab'),
                'You are missing Scrap metal and Fabric and a Light Vest in order to make a Reinforced Vest.',
                LineBreak(),
                ' ',
                Button('Leave Synthesizing Object', synthesize_object),
                float_right(Button('Check Pockets', pockets, margin_right=87)),
                float_right(Button('View Player Card', player_card, margin_right=5)),
            ])

@route
def make_torch(state:State)->Page:
    if 'Scrap Metal' in state.pockets and 'Lens' in state.pockets:
        state.pockets.remove('Scrap Metal')
        state.pockets.remove('Lens')
        state.pockets.append('Torch')
        return Page(state, content=[
            Header('Science Lab'),
            'You made a Torch!',
            LineBreak(),
            ' ',
            Button('Finish Synthesizing Object', synthesize_object),
            float_right(Button('Check Pockets', pockets, margin_right=87)),
            float_right(Button('View Player Card', player_card, margin_right=5)),
        ])
    elif 'Scrap Metal' in state.pockets and 'Lens' not in state.pockets:
        return Page(state, content=[
            Header('Science Lab'),
            'You are missing a Lens to make a Torch.',
            LineBreak(),
            ' ',
            Button('Leave Synthesizing Object', synthesize_object),
            float_right(Button('Check Pockets', pockets, margin_right=87)),
            float_right(Button('View Player Card', player_card, margin_right=5)),
        ])
    elif 'Scrap Metal' not in state.pockets and 'Lens' in state.pockets:
        return Page(state, content=[
            Header('Science Lab'),
            'You are missing Scrap Metal to make a Torch.',
            LineBreak(),
            ' ',
            Button('Leave Synthesizing Object', synthesize_object),
            float_right(Button('Check Pockets', pockets, margin_right=87)),
            float_right(Button('View Player Card', player_card, margin_right=5)),
        ])
    elif 'Scrap Metal' not in state.pockets and 'Lens' not in state.pockets:
        return Page(state, content=[
            Header('Science Lab'),
            'You are missing Scrap Metal and a Lens to make a Torch.',
            LineBreak(),
            ' ',
            Button('Leave Synthesizing Object', synthesize_object),
            float_right(Button('Check Pockets', pockets, margin_right=87)),
            float_right(Button('View Player Card', player_card, margin_right=5)),
        ])

@route
def make_crowbar(state:State)->Page:
    if 'Scrap Metal' in state.pockets and 'Piping' in state.pockets:
        state.pockets.remove('Scrap Metal')
        state.pockets.remove('Piping')
        state.pockets.append('Crowbar')
        return Page(state, content=[
            Header('Science Lab'),
            'You made a Crowbar!',
            LineBreak(),
            ' ',
            Button('Finish Synthesizing Object', synthesize_object),
            float_right(Button('Check Pockets', pockets, margin_right=87)),
            float_right(Button('View Player Card', player_card, margin_right=5)),
        ])
    elif 'Scrap Metal' in state.pockets and 'Piping' not in state.pockets:
        return Page(state, content=[
            Header('Science Lab'),
            'You are missing Piping to make a Crowbar.',
            LineBreak(),
            ' ',
            Button('Leave Synthesizing Object', synthesize_object),
            float_right(Button('Check Pockets', pockets, margin_right=87)),
            float_right(Button('View Player Card', player_card, margin_right=5)),
        ])
    elif 'Scrap Metal' not in state.pockets and 'Piping' in state.pockets:
        return Page(state, content=[
            Header('Science Lab'),
            'You are missing Scrap Metal to make a Crowbar.',
            LineBreak(),
            ' ',
            Button('Leave Synthesizing Object', synthesize_object),
            float_right(Button('Check Pockets', pockets, margin_right=87)),
            float_right(Button('View Player Card', player_card, margin_right=5)),
        ])
    elif 'Scrap Metal' not in state.pockets and 'Piping' not in state.pockets:
        return Page(state, content=[
            Header('Science Lab'),
            'You are missing Scrap Metal and Piping to make a Crowbar.',
            LineBreak(),
            ' ',
            Button('Leave Synthesizing Object', synthesize_object),
            float_right(Button('Check Pockets', pockets, margin_right=87)),
            float_right(Button('View Player Card', player_card, margin_right=5)),
        ])

@route
def lab_manual(state:State)->Page:
    state.last_location = 'lab_manual'
    Table_Header = ['Material 1', 'Material 2', 'Material 3', 'Created Material', 'Use Description']
    Life_Support = ['Empty Injector', 'Inaprolavine', '---', 'Life Boost', '+2 Max Health']
    Strength_Boost = ['Empty Injector', 'Hyperzine', '---', 'Strength Boost', '+2 Max Damage']
    Reinforced_Vest = ['Scrap Metal', 'Fabric', 'Light Vest', 'Reinforced Vest', '+2 Armor']
    Torch = ['Scrap Metal', 'Lens', '---', 'Torch', '-2 Max Damage, +Burn']
    Crowbar = ['Scrap Metal', 'Piping', '---', 'Crowbar', 'x3 Damage, -Combat Turn']
    return Page(state, content=[
        Header('Lab Manual'),
        Table([Table_Header, Life_Support, Strength_Boost, Reinforced_Vest, Torch, Crowbar]),
        'Note: You will need to equip/use any items made through the Player Card or Equipped Menus',
        LineBreak(),
        ' ',
        Button('Close Lab Manual', Science_Lab),
        float_right(Button('Check Pockets', pockets)),
        float_right(Button('View Player Card', player_card, margin_right=5)),
    ])
        

#Science Level ^ -------------------------------- Crew Level ⌄ --------------------------------------------------

@route
def Crew_Level(state:State)->Page:
    state.last_location = 'Crew_Level'
    return Page(state, content=[
        Header('Crew Level'),
        'Where on the Crew Level would you like to go?',
        Button('Mess Hall', Mess_Hall),
        Button('Quarters', Quarters),
        Button("Bar", Bar),
        LineBreak(),
        ' ',
        float_right(Button('Check Pockets', pockets, margin_right=87)),
        float_right(Button('View Player Card', player_card, margin_right=5)),
        Button('Back to Elevator', Elevator)
    ])

@route
def Mess_Hall(state:State)->Page:
    state.last_location = 'Mess_Hall'
    if not state.enemy_3_defeated:
        return Page(state, content=[
            Header("Mess Hall - ALERT"),
            "A hostile boarder is destroying the food replicators! Defend yourself.",
            LineBreak(),
            Button('Engage in Combat', setup_combat_3)
        ]) 
    elif state.enemy_3_defeated:
        return Page(state, content=[
            Header("Mess Hall"),
            'The enemy is out cold among the replicated food trays. The room is safe.',
            LineBreak(),
            ' ',
            float_right(Button('Check Pockets', pockets, margin_right=87)),
            float_right(Button('View Player Card', player_card, margin_right=5)),
            Button('Exit Mess Hall', Crew_Level)
        ])

@route
def setup_combat_3(state:State)->Page:
    state.current_enemy = 3
    state.current_burn_value = 0
    return combat_loop(state)

@route
def Quarters(state:State)->Page:
    state.last_location = 'Quarters'
    return Page(state, content=[
        Header('Quarters Corridor'),
        'You enter a hallway with three Quarters. Which Quarter would you like to search?',
        Button('Quarter 1', quarter1),
        Button('Quarter 2', quarter2),
        Button('Quarter 3', quarter3),
        LineBreak(),
        ' ',
        float_right(Button('Check Pockets', pockets, margin_right=87)),
        float_right(Button('View Player Card', player_card, margin_right=5)),
        Button('Exit Hallway', Crew_Level)
    ])

@route
def quarter1(state:State)->Page:
    state.last_location = 'quarter1'
    if not state.quarter1_fixed:
        if 'Spare Hinges' not in state.pockets and 'Tool Box' in state.pockets:
            return Page(state, content=[
                Header('Quarter 1'),
                'It appears that the door hinges are broken and need to be fixed.',
                LineBreak(),
                ' ',
                float_right(Button('Check Pockets', pockets, margin_right=87)),
                float_right(Button('View Player Card', player_card, margin_right=5)),
                Button('Exit Quarter 1', Quarters)
            ])
        elif 'Spare Hinges' in state.pockets and 'Tool Box' not in state.pockets:
            return Page(state, content=[
                Header('Quarter 1'),
                'You are missing the proper tools to fix the door.',
                LineBreak(),
                ' ',
                float_right(Button('Check Pockets', pockets, margin_right=87)),
                float_right(Button('View Player Card', player_card, margin_right=5)),
                Button('Exit Quarter 1', Quarters)
            ])
        elif 'Spare Hinges' not in state.pockets and 'Tool Box' not in state.pockets:
            return Page(state, content=[
                Header('Quarter 1'),
                'It appears the door hinges are broken and need to be fixed, and you do not have the proper tools.',
                LineBreak(),
                ' ',
                float_right(Button('Check Pockets', pockets, margin_right=87)),
                float_right(Button('View Player Card', player_card, margin_right=5)),
                Button('Exit Quarter 1', Quarters)
            ])
        elif 'Spare Hinges' in state.pockets and 'Tool Box' in state.pockets:
            state.quarter1_fixed = True
            state.pockets.remove('Spare Hinges')
            state.total_objectives_complete += 1
            return Page(state, content=[
                Header('Quarter 1'),
                'You fixed the door! What would you like to do in Quarter 1?',
                Button('Search Quarter 1', quarter1_search),
                LineBreak(),
                ' ',
                float_right(Button('Check Pockets', pockets, margin_right=87)),
                float_right(Button('View Player Card', player_card, margin_right=5)),
                Button('Exit Quarter 1', Quarters)
            ])
    elif state.quarter1_fixed:
        return Page(state, content=[
            Header('Quarter 1'),
            'What would you like to do in Quarter 1?',
            Button('Search Quarter 1', quarter1_search),
            LineBreak(),
            ' ',
            float_right(Button('Check Pockets', pockets, margin_right=87)),
            float_right(Button('View Player Card', player_card, margin_right=5)),
            Button('Exit Quarter 1', Quarters)
        ])

@route
def quarter1_search(state:State)->Page:
    state.last_location = 'quarter1_search'
    if not state.quarter1_searched:
        state.pockets.append('Spare Doorknob')
        state.pockets.append('Fabric')
        state.quarter1_searched = True
        return Page(state, content=[
            Header('Quarter 1'),
            'You found some extra Fabric in the closet and a Spare Doorknob in the dresser!',
            LineBreak(),
            ' ',
            Button('Finish Searching', quarter1),
            float_right(Button('Check Pockets', pockets, margin_right=87)),
            float_right(Button('View Player Card', player_card, margin_right=5)),
        ])
    elif state.quarter1_searched:
        return Page(state, content=[
            Header('Quarter 1'),
            'There is nothing else in Quarter 1',
            LineBreak(),
            ' ',
            Button('Finish Searching', quarter1),
            float_right(Button('Check Pockets', pockets, margin_right=87)),
            float_right(Button('View Player Card', player_card, margin_right=5)),
        ])

@route
def quarter2(state:State)->Page:
    state.last_location = 'quarter2'
    if not state.quarter2_fixed:
        if 'Spare Doorknob' not in state.pockets and 'Tool Box' in state.pockets:
            return Page(state, content=[
                Header('Quarter 2'),
                'It appears that the doorknob is missing and needs to be replaced.',
                LineBreak(),
                ' ',
                float_right(Button('Check Pockets', pockets, margin_right=87)),
                float_right(Button('View Player Card', player_card, margin_right=5)),
                Button('Exit Quarter 2', Quarters)
            ])
        elif 'Spare Doorknob' in state.pockets and 'Tool Box' not in state.pockets:
            return Page(state, content=[
                Header('Quarter 2'),
                'You are missing the proper tools to fix the door.',
                LineBreak(),
                ' ',
                float_right(Button('Check Pockets', pockets, margin_right=87)),
                float_right(Button('View Player Card', player_card, margin_right=5)),
                Button('Exit Quarter 2', Quarters)
            ])
        elif 'Spare Doorknob' not in state.pockets and 'Tool Box' not in state.pockets:
            return Page(state, content=[
                Header('Quarter 2'),
                'It appears the doorknob is missing and needs to be replaced, and you do not have the proper tools.',
                LineBreak(),
                ' ',
                float_right(Button('Check Pockets', pockets, margin_right=87)),
                float_right(Button('View Player Card', player_card, margin_right=5)),
                Button('Exit Quarter 2', Quarters)
            ])
        elif 'Spare Doorknob' in state.pockets and 'Tool Box' in state.pockets:
            state.quarter2_fixed = True
            state.total_objectives_complete += 1
            state.pockets.remove('Spare Doorknob')
            return Page(state, content=[
                Header('Quarter 2'),
                'You fixed the door! What would you like to do in Quarter 2?',
                Button('Search Quarter 2', quarter2_search),
                LineBreak(),
                ' ',
                float_right(Button('Check Pockets', pockets, margin_right=87)),
                float_right(Button('View Player Card', player_card, margin_right=5)),
                Button('Exit Quarter 2', Quarters)
            ])
    elif state.quarter2_fixed:
        return Page(state, content=[
            Header('Quarter 2'),
            'What would you like to do in Quarter 2?',
            Button('Search Quarter 2', quarter2_search),
            LineBreak(),
            ' ',
            float_right(Button('Check Pockets', pockets, margin_right=87)),
            float_right(Button('View Player Card', player_card, margin_right=5)),
            Button('Exit Quarter 2', Quarters)
        ])

@route
def quarter2_search(state:State)->Page:
    state.last_location = 'quarter2_search'
    if not state.quarter2_searched:
        state.pockets.append('Lens')
        state.quarter2_searched = True
        return Page(state, content=[
            Header('Quarter 2'),
            'You found a Lens in the bathroom!',
            LineBreak(),
            ' ',
            Button('Finish Searching', quarter2),
            float_right(Button('Check Pockets', pockets, margin_right=87)),
            float_right(Button('View Player Card', player_card, margin_right=5)),
        ])
    elif state.quarter2_searched:
        return Page(state, content=[
            Header('Quarter 2'),
            'There is nothing else in Quarter 2',
            LineBreak(),
            ' ',
            Button('Finish Searching', quarter2),
            float_right(Button('Check Pockets', pockets, margin_right=87)),
            float_right(Button('View Player Card', player_card, margin_right=5)),
        ])

@route
def quarter3(state:State)->Page:
    state.last_location = 'quarter3'
    if not state.enemy_4_defeated:
        return Page(state, content=[
            Header("Quarter 3 - ALERT"),
            "An enemy ambushes you from behind the closet door! Prepare to fight.",
            LineBreak(),
            Button('Engage in Combat', setup_combat_4)
        ])
    elif state.enemy_4_defeated:
        return Page(state, content=[
            Header("Quarter 3"),
            'The ambush failed. The enemy is neutralized on the floor.',
            LineBreak(),
            ' ',
            float_right(Button('Check Pockets', pockets, margin_right=87)),
            float_right(Button('View Player Card', player_card, margin_right=5)),
            Button('Exit Quarter 3', Quarters)
        ])

@route
def setup_combat_4(state:State)->Page:
    state.current_enemy = 4
    state.current_burn_value = 0
    return combat_loop(state)

@route
def Bar(state:State)->Page:
    state.last_location = 'Bar'
    return Page(state, content=[
        Header('Bar'),
        'What would you like to do at the Bar?',
        Button('Search the Bar', bar_search),
        Button('Have a Drink', take_drink),
        LineBreak(),
        ' ',
        float_right(Button('Check Pockets', pockets, margin_right=87)),
        float_right(Button('View Player Card', player_card, margin_right=5)),
        Button('Exit Storage', Science_Level),
    ])

@route
def bar_search(state:State)->Page:
    state.last_location = 'bar_search'
    if not state.bar_searched:
        state.bar_searched = True
        state.pockets.append('Spare Glass')
        state.pockets.append('Terminal Code Note')
        return Page(state, content=[
            Header('Bar'),
            'You found some Spare Glass and a Terminal Code Note!',
            LineBreak(),
            ' ',
            float_right(Button('Check Pockets', pockets, margin_right=87)),
            float_right(Button('View Player Card', player_card, margin_right=5)),
            Button('Finish Searching', Bar),
        ])
    elif state.bar_searched:
        return Page(state, content=[
            Header('Bar'),
            'There is nothing else to find at the Bar',
            LineBreak(),
            ' ',
            float_right(Button('Check Pockets', pockets, margin_right=87)),
            float_right(Button('View Player Card', player_card, margin_right=5)),
            Button('Finish Searching', Bar),
        ])

@route
def take_drink(state:State)->Page:
    if state.current_total_drinks == 3:
        return Page(state, content=[
            Header('Bar'),
            'There are no more drinks at the bar.',
            LineBreak(),
            ' ',
            float_right(Button('Check Pockets', pockets, margin_right=87)),
            float_right(Button('View Player Card', player_card, margin_right=5)),
            Button('Stop Drinking', Bar),
        ])
    elif state.current_total_drinks < 3:
        state.current_total_drinks += 1
        rolled_value = drink_roll()
        if rolled_value == 1:
            rolled_drink = 'some 100 Year Aged Cognac'
            result = 'gained 5 Max Health!'
            state.player_max_health += 5
            state.player_current_health += 5
        elif rolled_value in range(2,26):
            rolled_drink = 'a Chilled Beer'
            state.player_max_health += 2
            state.player_current_health += 2
            result = 'gained 2 Max Health!'
        elif rolled_value == 26:
            rolled_drink = 'some Heavily Spoiled Champagne'
            state.player_max_health -= 5
            state.player_current_health -= 5
            result = 'lost 5 Max Health.'
            if state.player_current_health <= 0:
                return drinking_loss(state)
        elif rolled_value in range(27,51):
            rolled_drink = 'a Rum and Coke (left out overnight)'
            state.player_max_health -= 2
            state.player_current_health -= 2
            result = 'lost 2 Max Health.'
            if state.player_current_health <= 0:
                return drinking_loss_health(state)
        elif rolled_value == 51:
            rolled_drink = 'some Aged Bourbon'
            state.player_max_damage += 5
            result = 'gained 5 Max Damage!'
        elif rolled_value in range(52,76):
            rolled_drink = 'an Espresso Martini'
            state.player_max_damage += 2
            result = 'gained 2 Max Damage!'
        elif rolled_value == 76:
            rolled_drink = 'a Spiked Drink'
            state.player_max_damage -= 5
            result = 'lost 5 Max Damage.'
            if state.player_max_damage <= 0:
                return loss_damage(state)
        elif rolled_value in range(77,101):
            rolled_drink = 'an Everclear Shot'
            state.player_max_damage -= 2
            result = 'lost 2 Max Damage.'
            if state.player_max_damage <= 0:
                return loss_damage(state)
        return Page(state, content=[
            Header('Bar'),
            'You found ' + rolled_drink,
            'You ' + result,
            LineBreak(),
            ' ',
            float_right(Button('Check Pockets', pockets, margin_right=87)),
            float_right(Button('View Player Card', player_card, margin_right=5)),
            Button('Have Another Drink', take_drink),
            Button('Stop Drinking', Bar),
        ])
    
#Crew Level ^ -------------------------------- Security Level ⌄ --------------------------------------------------    

@route
def Security_Level(state:State)->Page:
    state.last_location = "Security_Level"
    return Page(state, content=[
        Header('Security Level'),
        'Where on the Security Level would you like to go?',
        Button('Armory', Armory),
        Button('Jail', Jail),
        LineBreak(),
        ' ',
        float_right(Button('Check Pockets', pockets, margin_right=87)),
        float_right(Button('View Player Card', player_card, margin_right=5)),
        Button('Back to Elevator', Elevator)
    ])

@route
def Armory(state:State)->Page:
    state.last_location = 'Armory'
    return Page(state, content=[
        Header('Armory'),
        'What would you like to do in the Armory?',
        Button('Search the Armory', armory_search),
        LineBreak(),
        ' ',
        float_right(Button('Check Pockets', pockets, margin_right=87)),
        float_right(Button('View Player Card', player_card, margin_right=5)),
        Button('Exit Armory', Security_Level),
    ])

@route
def armory_search(state:State)->Page:
    state.last_location = 'armory_search'
    if not state.armory_searched:
        state.armory_searched = True
        state.pockets.append('Light Vest')
        state.pockets.append('Basic Phaser')
        return Page(state, content=[
            Header('Armory'),
            'You found a Light Vest and a Basic Phaser!',
            'Note: You will need to equip these items (accessible though the pockets menu)',
            LineBreak(),
            ' ',
            float_right(Button('Check Pockets', pockets, margin_right=87)),
            float_right(Button('View Player Card', player_card, margin_right=5)),
            Button('Finish Searching', Armory),
        ])
    elif state.armory_searched:
        return Page(state, content=[
            Header('Armory'),
            'There is nothing else to find in the Armory',
            LineBreak(),
            ' ',
            float_right(Button('Check Pockets', pockets, margin_right=87)),
            float_right(Button('View Player Card', player_card, margin_right=5)),
            Button('Finish Searching', Armory),
        ])

@route
def Jail(state:State)->Page:
    state.last_location = 'Jail'
    if not state.enemy_5_defeated:
        return Page(state, content=[
            Header("Jail - ALERT"),
            "A saboteur is trying to drop the security forcefields! Stop them immediately.",
            LineBreak(),
            Button('Engage in Combat', setup_combat_5)
        ])
    elif state.enemy_5_defeated:
        return Page(state, content=[
            Header("Jail"),
            'The saboteur has been incapacitated and ironically locked inside a cell.',
            LineBreak(),
            ' ',
            float_right(Button('Check Pockets', pockets, margin_right=87)),
            float_right(Button('View Player Card', player_card, margin_right=5)),
            Button('Search Jail', jail_search),
            Button('Exit Jail', Security_Level)
        ])

@route
def setup_combat_5(state:State)->Page:
    state.current_enemy = 5
    state.current_burn_value = 0
    return combat_loop(state)

@route
def jail_search(state:State)->Page:
    state.last_location = 'jail_search'
    if not state.jail_searched:
        state.jail_searched = True
        state.pockets.append('Scrap Metal')
        state.pockets.append('Scrap Metal')
        return Page(state, content=[
            Header('Elevator'),
            'You found some Scrap Metal!',
            LineBreak(),
            ' ',
            Button('Finish Searching', Jail),
            float_right(Button('Check Pockets', pockets, margin_right=87)),
            float_right(Button('View Player Card', player_card, margin_right=5)),
        ])
    elif state.jail_searched:
        return Page(state, content=[
            Header('Elevator'),
            'There is nothing left to find in the Jail.',
            LineBreak(),
            ' ',
            Button('Finish Searching', Jail),
            float_right(Button('Check Pockets', pockets, margin_right=87)),
            float_right(Button('View Player Card', player_card, margin_right=5)),
        ])
    
#Security Level^ ---------------------------------------- Combat System⌄-------------------------------------------------

@route
def combat_loop(state:State)->Page:
    current_e_health = 0
    if state.current_enemy == 1:
        current_e_health = state.enemy_1_health
    elif state.current_enemy == 2:
        current_e_health = state.enemy_2_health
    elif state.current_enemy == 3:
        current_e_health = state.enemy_3_health
    elif state.current_enemy == 4:
        current_e_health = state.enemy_4_health
    elif state.current_enemy == 5:
        current_e_health = state.enemy_5_health
    return Page(state, content=[
        Header('COMBAT ENGAGED'),
        'You are fighting Enemy ' + str(state.current_enemy),
        LineBreak(),
        'Your Health: ' + str(state.player_current_health) + ' / ' + str(state.player_max_health),
        'Enemy Health: ' + str(current_e_health),
        LineBreak(),
        'Equipped Weapon: ' + state.equipped_weapon,
        'Equipped Armor: ' + state.equipped_armor,
        LineBreak(),
        ' ',
        Button('ATTACK!', resolve_combat_turn),
    ])

@route
def resolve_combat_turn(state:State)->Page:
    player_roll_1 = randint(1, state.player_max_damage)
    total_player_damage = player_roll_1 + state.player_damage_buff
    if state.equipped_weapon == 'Crowbar':
        total_player_damage = (player_roll_1 * 3) + state.player_damage_buff   
    elif state.equipped_weapon == 'Basic Phaser' and state.phaser_setting == 'Stun':
        player_roll_2 = randint(1, state.player_max_damage)
        total_player_damage = player_roll_1 + player_roll_2 + state.player_damage_buff
    elif state.equipped_weapon == 'Torch':
        total_player_damage += state.current_burn_value
        state.current_burn_value += 2
    if state.current_enemy == 1:
        state.enemy_1_health -= total_player_damage
    elif state.current_enemy == 2:
        state.enemy_2_health -= total_player_damage
    elif state.current_enemy == 3:
        state.enemy_3_health -= total_player_damage
    elif state.current_enemy == 4:
        state.enemy_4_health -= total_player_damage
    elif state.current_enemy == 5:
        state.enemy_5_health -= total_player_damage
    enemy_is_dead = False
    if state.current_enemy == 1 and state.enemy_1_health <= 0:
        enemy_is_dead = True
    elif state.current_enemy == 2 and state.enemy_2_health <= 0:
        enemy_is_dead = True
    elif state.current_enemy == 3 and state.enemy_3_health <= 0:
        enemy_is_dead = True
    elif state.current_enemy == 4 and state.enemy_4_health <= 0:
        enemy_is_dead = True
    elif state.current_enemy == 5 and state.enemy_5_health <= 0:
        enemy_is_dead = True
    if enemy_is_dead:
        return combat_victory(state)
    enemy_roll = randint(1, 8)
    total_enemy_damage = enemy_roll
    if state.equipped_weapon == 'Crowbar':
        enemy_roll_2 = randint(1, 8)
        total_enemy_damage += enemy_roll_2
    total_enemy_damage -= state.player_armor
    if total_enemy_damage < 0:
        total_enemy_damage = 0
    state.player_current_health -= total_enemy_damage
    if state.player_current_health <= 0:
        return combat_loss(state)
    return combat_loop(state)

@route
def combat_victory(state:State)->Page:
    if state.current_enemy == 1:
        state.enemy_1_defeated = True
    elif state.current_enemy == 2:
        state.enemy_2_defeated = True
    elif state.current_enemy == 3:
        state.enemy_3_defeated = True
    elif state.current_enemy == 4:
        state.enemy_4_defeated = True
    elif state.current_enemy == 5:
        state.enemy_5_defeated = True
    state.total_enemies_defeated += 1
    return Page(state, content=[
        Header('Enemy Defeated!'),
        'You have successfully defeated the enemy! The area is safe.',
        LineBreak(),
        ' ',
        Button('Return to Room', state.last_location) 
    ])


set_website_style('sakura')
hide_debug_information()
start_server(initial_state)
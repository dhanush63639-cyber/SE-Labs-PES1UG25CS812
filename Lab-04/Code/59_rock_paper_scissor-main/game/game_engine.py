import random
import math
import pygame
from game.button import ChoiceButton
from game.icons import draw_icon, draw_fist, draw_question

class GameEngine:
    def __init__(self, width, height):
        self.width = width
        self.height = height

        self.choices = ["ROCK", "PAPER", "SCISSORS"]
        btn_w, btn_h = 130, 50
        gap = 20
        total_w = 3 * btn_w + 2 * gap
        start_x = (width - total_w) // 2
        btn_y = height - 85

        self.buttons = [
            ChoiceButton("ROCK", pygame.Rect(start_x, btn_y, btn_w, btn_h), (160, 50, 50), (200, 70, 70)),
            ChoiceButton("PAPER", pygame.Rect(start_x + btn_w + gap, btn_y, btn_w, btn_h), (40, 100, 170), (60, 130, 210)),
            ChoiceButton("SCISSORS", pygame.Rect(start_x + 2 * (btn_w + gap), btn_y, btn_w, btn_h), (180, 140, 30), (220, 180, 50)),
        ]

        self.player_choice = None
        self.cpu_choice = None
        self.result_text = "Make your move!"
        self.result_color = (220, 225, 235)

        self.player_score = 0
        self.cpu_score = 0
        self.target_score = 5
        self.match_over = False
        self.match_winner = None

        self.round_resolved_time = 0
        self.display_duration = 1800
        self.showing_result = False

        self.animating = False
        self.anim_start_time = 0
        self.anim_duration = 1200
        self.pending_player = None
        self.pending_cpu = None

        self.player_history = []
        self.history_window = 10
        self.counter_map = {"ROCK": "PAPER", "PAPER": "SCISSORS", "SCISSORS": "ROCK"}

        self.font_countdown = pygame.font.SysFont(None, 56)

        self.font_title = pygame.font.SysFont(None, 36)
        self.font_hud = pygame.font.SysFont(None, 26)
        self.font_arena = pygame.font.SysFont(None, 32)
        self.font_banner = pygame.font.SysFont(None, 48)
        self.font_hint = pygame.font.SysFont(None, 24)

    def determine_winner(self, player, cpu):
        if player == cpu:
            return "TIE"
            
        rules = {
            ("ROCK", "SCISSORS"): "PLAYER",
            ("SCISSORS", "PAPER"): "PLAYER",
            ("PAPER", "ROCK"): "PLAYER",
            ("SCISSORS", "ROCK"): "CPU",
            ("PAPER", "SCISSORS"): "CPU",
            ("ROCK", "PAPER"): "CPU",
        }
        return rules.get((player, cpu), "TIE")

    def cpu_pick(self):
        """Adaptive CPU choice: bias toward counter of player's most frequent recent move."""
        recent = self.player_history[-self.history_window:]
        if len(recent) < 3:
            return random.choice(self.choices)

        counts = {c: recent.count(c) for c in self.choices}
        favorite = max(counts, key=counts.get)

        if counts[favorite] / len(recent) > 0.5:
            if random.random() < 0.70:
                return self.counter_map[favorite]

        return random.choice(self.choices)

    def reset_match(self):
        self.player_score = 0
        self.cpu_score = 0
        self.player_choice = None
        self.cpu_choice = None
        self.result_text = "Make your move!"
        self.result_color = (220, 225, 235)
        self.match_over = False
        self.match_winner = None
        self.showing_result = False
        self.animating = False
        self.pending_player = None
        self.pending_cpu = None
        self.player_history = []

    def start_round(self, choice):
        """Store choices and begin the countdown animation."""
        self.pending_player = choice
        self.pending_cpu = self.cpu_pick()
        self.player_history.append(choice)
        self.animating = True
        self.anim_start_time = pygame.time.get_ticks()

    def resolve_round(self):
        """Evaluate outcome after the animation finishes."""
        self.player_choice = self.pending_player
        self.cpu_choice = self.pending_cpu
        self.animating = False

        outcome = self.determine_winner(self.player_choice, self.cpu_choice)
        if outcome == "PLAYER":
            self.player_score += 1
            self.result_text = f"You Win! {self.player_choice} beats {self.cpu_choice}."
            self.result_color = (80, 230, 120)
        elif outcome == "CPU":
            self.cpu_score += 1
            self.result_text = f"You Lose! {self.cpu_choice} beats {self.player_choice}."
            self.result_color = (240, 80, 80)
        else:
            self.result_text = f"It's a Draw! Both picked {self.player_choice}."
            self.result_color = (240, 210, 80)

        self.showing_result = True
        self.round_resolved_time = pygame.time.get_ticks()

        if self.player_score >= self.target_score:
            self.match_over = True
            self.match_winner = "PLAYER"
        elif self.cpu_score >= self.target_score:
            self.match_over = True
            self.match_winner = "CPU"

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_r and self.match_over:
            self.reset_match()
            return

        if self.match_over or self.animating or self.showing_result:
            return

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            for btn in self.buttons:
                if btn.contains(event.pos):
                    self.start_round(btn.choice_name)
                    break

    def update(self):
        now = pygame.time.get_ticks()
        if self.animating and (now - self.anim_start_time >= self.anim_duration):
            self.resolve_round()
        if self.showing_result and (now - self.round_resolved_time >= self.display_duration):
            self.player_choice = None
            self.cpu_choice = None
            self.result_text = "Make your move!"
            self.result_color = (190, 195, 205)
            self.showing_result = False

    def render(self, screen):
        screen.fill((24, 28, 36))
        now = pygame.time.get_ticks()

        title_surf = self.font_title.render("Rock Paper Scissors", True, (245, 245, 245))
        screen.blit(title_surf, (self.width // 2 - title_surf.get_width() // 2, 14))

        target_surf = self.font_hud.render(f"First to {self.target_score}", True, (180, 180, 190))
        screen.blit(target_surf, (self.width // 2 - target_surf.get_width() // 2, 52))

        p_surf = self.font_hud.render(f"Player: {self.player_score}", True, (100, 180, 255))
        c_surf = self.font_hud.render(f"CPU: {self.cpu_score}", True, (255, 120, 120))
        screen.blit(p_surf, (35, 52))
        screen.blit(c_surf, (self.width - c_surf.get_width() - 35, 52))

        pygame.draw.line(screen, (45, 52, 66), (25, 82), (self.width - 25, 82), 2)

        # --- Arena with procedural icons ---
        icon_size = 30
        p_ix = self.width // 4
        c_ix = 3 * self.width // 4
        icon_y = 145

        # Side labels
        you_lbl = self.font_hud.render("YOU", True, (100, 180, 255))
        cpu_lbl = self.font_hud.render("CPU", True, (255, 120, 120))
        screen.blit(you_lbl, (p_ix - you_lbl.get_width() // 2, 90))
        screen.blit(cpu_lbl, (c_ix - cpu_lbl.get_width() // 2, 90))

        if self.animating:
            elapsed = now - self.anim_start_time
            phase = min(int(elapsed / 400), 2)
            countdown_num = 3 - phase
            shake_y = int(math.sin(elapsed * 0.018) * 10)

            draw_fist(screen, p_ix, icon_y, icon_size, shake_y)
            draw_fist(screen, c_ix, icon_y, icon_size, shake_y)

            cd_surf = self.font_countdown.render(str(countdown_num), True, (255, 220, 80))
            screen.blit(cd_surf, (self.width // 2 - cd_surf.get_width() // 2,
                                  icon_y - cd_surf.get_height() // 2))
        elif self.showing_result:
            draw_icon(screen, self.player_choice, p_ix, icon_y, icon_size)
            draw_icon(screen, self.cpu_choice, c_ix, icon_y, icon_size)

            pn = self.font_hint.render(self.player_choice, True, (200, 205, 215))
            cn = self.font_hint.render(self.cpu_choice, True, (200, 205, 215))
            screen.blit(pn, (p_ix - pn.get_width() // 2, icon_y + icon_size + 12))
            screen.blit(cn, (c_ix - cn.get_width() // 2, icon_y + icon_size + 12))

            vs_surf = self.font_arena.render("VS", True, (80, 85, 100))
            screen.blit(vs_surf, (self.width // 2 - vs_surf.get_width() // 2,
                                  icon_y - vs_surf.get_height() // 2))
        else:
            draw_question(screen, p_ix, icon_y, icon_size)
            draw_question(screen, c_ix, icon_y, icon_size)

            vs_surf = self.font_arena.render("VS", True, (60, 65, 78))
            screen.blit(vs_surf, (self.width // 2 - vs_surf.get_width() // 2,
                                  icon_y - vs_surf.get_height() // 2))

        # Result text
        res_surf = self.font_arena.render(self.result_text, True, self.result_color)
        screen.blit(res_surf, (self.width // 2 - res_surf.get_width() // 2, 215))

        # Buttons (hidden during animation and match-over)
        if not self.match_over and not self.animating and not self.showing_result:
            for btn in self.buttons:
                btn.render(screen)

        if self.match_over:
            overlay = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 160))
            screen.blit(overlay, (0, 0))

            if self.match_winner == "PLAYER":
                banner_text = "YOU WIN THE MATCH!"
                banner_color = (80, 230, 120)
            else:
                banner_text = "CPU WINS THE MATCH!"
                banner_color = (240, 80, 80)

            banner_surf = self.font_banner.render(banner_text, True, banner_color)
            screen.blit(banner_surf, (self.width // 2 - banner_surf.get_width() // 2, self.height // 2 - 30))

            score_text = f"Final Score  -  Player {self.player_score}  :  {self.cpu_score} CPU"
            score_surf = self.font_hud.render(score_text, True, (220, 220, 225))
            screen.blit(score_surf, (self.width // 2 - score_surf.get_width() // 2, self.height // 2 + 15))

            hint_surf = self.font_hint.render("Press R to play again", True, (160, 165, 175))
            screen.blit(hint_surf, (self.width // 2 - hint_surf.get_width() // 2, self.height // 2 + 50))

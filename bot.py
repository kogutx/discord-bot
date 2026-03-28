import os
import discord
from discord.ext import commands

intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

SUPPORT_ROLE_NAME = "⨯ Support"
TICKETS_CATEGORY_NAME = "Tickety"


# ===== POMOCNICZE =====

def sanitize_name(text: str) -> str:
    return text.lower().replace(" ", "-").replace("_", "-")

def get_support_role(guild: discord.Guild):
    return discord.utils.get(guild.roles, name=SUPPORT_ROLE_NAME)


def get_next_ticket_number(guild: discord.Guild) -> int:
    numbers = []

    for channel in guild.text_channels:
        if channel.name.startswith("ticket-"):
            parts = channel.name.split("-")
            if len(parts) >= 2 and parts[1].isdigit():
                numbers.append(int(parts[1]))

    if not numbers:
        return 1

    return max(numbers) + 1

async def create_ticket_channel(
    interaction: discord.Interaction,
    category_value: str,
    category_label: str,
    topic: str,
    description: str
):
    guild = interaction.guild
    user = interaction.user

    if guild is None:
        await interaction.response.send_message("To działa tylko na serwerze.", ephemeral=True)
        return

    support_role = get_support_role(guild)

    tickets_category = discord.utils.get(guild.categories, name=TICKETS_CATEGORY_NAME)
    if tickets_category is None:
        tickets_category = await guild.create_category(TICKETS_CATEGORY_NAME)

    for channel in guild.text_channels:
        if channel.name.startswith("ticket-"):
            overwrites_for_user = channel.overwrites_for(user)
            if overwrites_for_user.view_channel is True:
                await interaction.response.send_message(
                    f"Masz już otwarty ticket: {channel.mention}",
                    ephemeral=True
                )
                return

    ticket_number = get_next_ticket_number(guild)
    channel_name = f"ticket-{ticket_number}"

    overwrites = {
        guild.default_role: discord.PermissionOverwrite(view_channel=False),
        user: discord.PermissionOverwrite(
            view_channel=True,
            send_messages=True,
            read_message_history=True,
            attach_files=True,
            embed_links=True
        )
    }

    if support_role:
        overwrites[support_role] = discord.PermissionOverwrite(
            view_channel=True,
            send_messages=True,
            read_message_history=True,
            attach_files=True,
            embed_links=True,
            manage_channels=True,
            manage_messages=True
        )

    channel = await guild.create_text_channel(
        name=channel_name,
        category=tickets_category,
        overwrites=overwrites,
        topic=f"owner:{user.id};category:{category_value}"
    )

    embed = discord.Embed(
        title=f"{category_label} — Ticket #{ticket_number}",
        description=description,
        color=discord.Color.dark_gray()
    )
    embed.add_field(name="📋 Temat", value=topic, inline=False)
    embed.add_field(name="👤 Użytkownik", value=user.mention, inline=True)
    embed.add_field(name="🗂️ Kategoria", value=category_label, inline=True)
    embed.set_footer(text=f"Ticket #{ticket_number} • {guild.name} • System Ticketów")

    content = f"{user.mention}"
    if support_role:
        content += f" {support_role.mention}"
    content += " — Twój ticket został otwarty!"

    view = TicketButtonsView()

    await channel.send(
        content=content,
        embed=embed,
        view=view
    )

    await interaction.response.send_message(
        f"Ticket utworzony: {channel.mention}",
        ephemeral=True
    )
    return

    ticket_number = get_next_ticket_number(guild)
    channel_name = f"ticket-{ticket_number}"

    overwrites = {
        guild.default_role: discord.PermissionOverwrite(view_channel=False),
        user: discord.PermissionOverwrite(
            view_channel=True,
            send_messages=True,
            read_message_history=True,
            attach_files=True,
            embed_links=True
        )
    }

    if support_role:
        overwrites[support_role] = discord.PermissionOverwrite(
            view_channel=True,
            send_messages=True,
            read_message_history=True,
            attach_files=True,
            embed_links=True,
            manage_channels=True,
            manage_messages=True
        )

    channel = await guild.create_text_channel(
        name=channel_name,
        category=tickets_category,
        overwrites=overwrites,
        topic=f"owner:{user.id};category:{category_value}"
    )

    embed = discord.Embed(
        title=f"{category_label} — Ticket #{ticket_number}",
        description=description,
        color=discord.Color.dark_gray()
    )
    embed.add_field(name="📋 Temat", value=topic, inline=False)
    embed.add_field(name="👤 Użytkownik", value=user.mention, inline=True)
    embed.add_field(name="🗂️ Kategoria", value=category_label, inline=True)
    embed.set_footer(text=f"Ticket #{ticket_number} • {guild.name} • System Ticketów")

    content = f"{user.mention}"
    if support_role:
        content += f" {support_role.mention}"
    content += " — Twój ticket został otwarty!"

    view = TicketButtonsView()

    await channel.send(
        content=content,
        embed=embed,
        view=view
    )

    await interaction.response.send_message(
        f"Ticket utworzony: {channel.mention}",
        ephemeral=True
    )


    support_role = get_support_role(guild)

    overwrites = {
        guild.default_role: discord.PermissionOverwrite(view_channel=False),
        user: discord.PermissionOverwrite(
            view_channel=True,
            send_messages=True,
            read_message_history=True,
            attach_files=True,
            embed_links=True
        )
    }

    if support_role:
        overwrites[support_role] = discord.PermissionOverwrite(
            view_channel=True,
            send_messages=True,
            read_message_history=True,
            attach_files=True,
            embed_links=True,
            manage_channels=True,
            manage_messages=True
        )

    channel = await guild.create_text_channel(
        name=channel_name,
        category=tickets_category,
        overwrites=overwrites
    )

    embed = discord.Embed(
        title=f"📩 {category_label} — Ticket",
        description=description,
        color=discord.Color.dark_gray()
    )
    embed.add_field(name="📋 Temat", value=topic, inline=False)
    embed.add_field(name="👤 Użytkownik", value=user.mention, inline=True)
    embed.add_field(name="🗂️ Kategoria", value=category_label, inline=True)
    embed.set_footer(text=f"{guild.name} • System Ticketów")

    content = f"{user.mention}"
    if support_role:
        content += f" {support_role.mention}"

    view = TicketButtonsView()

    await channel.send(
        content=f"{content} — Twój ticket został otwarty!",
        embed=embed,
        view=view
    )

    await interaction.response.send_message(
        f"Ticket utworzony: {channel.mention}",
        ephemeral=True
    )


# ===== PRZYCISKI W TICKECIE =====

class TicketButtonsView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(
        label="Zamknij ticket",
        style=discord.ButtonStyle.danger,
        emoji="🔒",
        custom_id="ticket_close_button"
    )
    async def close_ticket(self, interaction: discord.Interaction, button: discord.ui.Button):
        channel = interaction.channel
        if channel is None or not channel.name.startswith("ticket-"):
            await interaction.response.send_message("To nie jest kanał ticketu.", ephemeral=True)
            return

        await interaction.response.send_message("Zamykam ticket...", ephemeral=True)
        await channel.delete()

    @discord.ui.button(
        label="Przejmij ticket",
        style=discord.ButtonStyle.primary,
        emoji="🫡",
        custom_id="ticket_claim_button"
    )
    async def claim_ticket(self, interaction: discord.Interaction, button: discord.ui.Button):
        guild = interaction.guild
        user = interaction.user

        if guild is None or interaction.channel is None:
            await interaction.response.send_message("Błąd.", ephemeral=True)
            return

        support_role = get_support_role(guild)

        has_access = False
        if isinstance(user, discord.Member):
            if user.guild_permissions.administrator:
                has_access = True
            elif support_role and support_role in user.roles:
                has_access = True

        if not has_access:
            await interaction.response.send_message("Tylko support może przejąć ticket.", ephemeral=True)
            return

        await interaction.response.send_message("Ticket został przejęty.", ephemeral=True)
        await interaction.channel.send(f"🫡 Ticket został przejęty przez {user.mention}.")


# ===== FORMULARZ =====

class TicketModal(discord.ui.Modal):
    def __init__(self, category_label: str, category_value: str):
        super().__init__(title=category_label)

        self.category_label = category_label
        self.category_value = category_value

        self.topic = discord.ui.TextInput(
            label="Temat",
            placeholder="Krótki opis sprawy",
            required=True,
            max_length=100
        )

        self.details = discord.ui.TextInput(
            label="Opis",
            placeholder="Opisz szczegółowo swoją sprawę...",
            style=discord.TextStyle.paragraph,
            required=True,
            max_length=1000
        )

        self.add_item(self.topic)
        self.add_item(self.details)

    async def on_submit(self, interaction: discord.Interaction):
        await create_ticket_channel(
            interaction=interaction,
            category_value=self.category_value,
            category_label=self.category_label,
            topic=str(self.topic),
            description=str(self.details)
        )


        # ===== REKRUTACJA SUPPORT =====

class SupportApplicationButtons(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(
        label="Zaakceptuj",
        style=discord.ButtonStyle.success,
        emoji="✅",
        custom_id="support_application_accept"
    )
    async def accept_application(self, interaction: discord.Interaction, button: discord.ui.Button):
        if not isinstance(interaction.user, discord.Member):
            await interaction.response.send_message("Błąd.", ephemeral=True)
            return

        if not interaction.user.guild_permissions.administrator:
            await interaction.response.send_message("Tylko administracja może to zrobić.", ephemeral=True)
            return

        if not interaction.message or not interaction.message.embeds:
            await interaction.response.send_message("Nie znaleziono danych podania.", ephemeral=True)
            return

        embed = interaction.message.embeds[0]
        applicant_id = None

        if embed.footer and embed.footer.text.startswith("applicant_id:"):
            try:
                applicant_id = int(embed.footer.text.replace("applicant_id:", "").strip())
            except ValueError:
                applicant_id = None

        if applicant_id is None:
            await interaction.response.send_message("Nie można odczytać ID użytkownika.", ephemeral=True)
            return

        guild = interaction.guild
        member = guild.get_member(applicant_id) if guild else None
        if member is None:
            await interaction.response.send_message("Nie znaleziono użytkownika na serwerze.", ephemeral=True)
            return

        role = discord.utils.get(guild.roles, name=SUPPORT_ROLE_NAME)
        if role is None:
            await interaction.response.send_message(
                f"Nie znaleziono roli `{SUPPORT_ROLE_NAME}`.",
                ephemeral=True
            )
            return

        await member.add_roles(role, reason=f"Akceptacja podania przez {interaction.user}")

        new_embed = discord.Embed(
            title="✅ Aplikacja na Support - Zaakceptowana!",
            description=(
                "Gratulacje! Twoja aplikacja na stanowisko **Support** została **zaakceptowana**.\n"
                "Rola została Ci automatycznie nadana."
            ),
            color=discord.Color.green()
        )

        await interaction.message.edit(embed=new_embed, view=None)
        await interaction.response.send_message("Podanie zaakceptowane.", ephemeral=True)

        try:
            dm_embed = discord.Embed(
                title="✅ Aplikacja na Support - Zaakceptowana!",
                description=(
                    "Gratulacje! Twoja aplikacja na stanowisko **Support** została **zaakceptowana**.\n"
                    "Rola została Ci automatycznie nadana."
                ),
                color=discord.Color.green()
            )
            await member.send(embed=dm_embed)
        except discord.Forbidden:
            pass

    @discord.ui.button(
        label="Odrzuć",
        style=discord.ButtonStyle.danger,
        emoji="❌",
        custom_id="support_application_reject"
    )
    async def reject_application(self, interaction: discord.Interaction, button: discord.ui.Button):
        if not isinstance(interaction.user, discord.Member):
            await interaction.response.send_message("Błąd.", ephemeral=True)
            return

        if not interaction.user.guild_permissions.administrator:
            await interaction.response.send_message("Tylko administracja może to zrobić.", ephemeral=True)
            return

        if not interaction.message or not interaction.message.embeds:
            await interaction.response.send_message("Nie znaleziono danych podania.", ephemeral=True)
            return

        embed = interaction.message.embeds[0]
        applicant_id = None

        if embed.footer and embed.footer.text.startswith("applicant_id:"):
            try:
                applicant_id = int(embed.footer.text.replace("applicant_id:", "").strip())
            except ValueError:
                applicant_id = None

        new_embed = discord.Embed(
            title="❌ Aplikacja na Support - Odrzucona!",
            description=(
                "Przykro nam! Twoja aplikacja na stanowisko **Support** została **odrzucona**.\n"
                "Powodzenia następnym razem!"
            ),
            color=discord.Color.red()
        )

        await interaction.message.edit(embed=new_embed, view=None)
        await interaction.response.send_message("Podanie odrzucone.", ephemeral=True)

        if applicant_id and interaction.guild:
            member = interaction.guild.get_member(applicant_id)
            if member:
                try:
                    dm_embed = discord.Embed(
                        title="❌ Aplikacja na Support - Odrzucona!",
                        description=(
                            "Przykro nam! Twoja aplikacja na stanowisko **Support** została **odrzucona**.\n"
                            "Powodzenia następnym razem!"
                        ),
                        color=discord.Color.red()
                    )
                    await member.send(embed=dm_embed)
                except discord.Forbidden:
                    pass

class SupportApplicationModal(discord.ui.Modal, title="Aplikuj na Support"):
    age = discord.ui.TextInput(
        label="Ile masz lat?",
        placeholder="np. 18",
        required=True,
        max_length=20
    )

    activity = discord.ui.TextInput(
        label="Ile dziennie czasu będziesz aktywny?",
        placeholder="np. 3-4 godziny",
        required=True,
        max_length=100
    )

    promotion = discord.ui.TextInput(
        label="Czy będziesz pomagał w promowaniu serwera?",
        placeholder="np. Tak, mogę promować na...",
        required=True,
        max_length=300
    )

    rules = discord.ui.TextInput(
        label="Czy znasz zasady serwera?",
        placeholder="np. Tak, znam regulamin",
        required=True,
        max_length=300
    )

    async def on_submit(self, interaction: discord.Interaction):
        guild = interaction.guild
        user = interaction.user

        if guild is None:
            await interaction.response.send_message("To działa tylko na serwerze.", ephemeral=True)
            return

        app_channel = guild.get_channel(1479745316705140736)
        if app_channel is None:
            await interaction.response.send_message(
                "Nie ustawiono poprawnie kanału na podania.",
                ephemeral=True
            )
            return

        embed = discord.Embed(
            title="📑 Nowe podanie na Support",
            color=discord.Color.dark_gray()
        )
        embed.add_field(name="👤 Użytkownik", value=f"{user.mention}\n`{user.id}`", inline=False)
        embed.add_field(name="🎂 Ile masz lat?", value=str(self.age), inline=False)
        embed.add_field(name="⏰ Ile dziennie czasu będziesz aktywny?", value=str(self.activity), inline=False)
        embed.add_field(name="📢 Czy będziesz pomagał w promowaniu serwera?", value=str(self.promotion), inline=False)
        embed.add_field(name="📘 Czy znasz zasady serwera?", value=str(self.rules), inline=False)
        embed.set_footer(text=f"applicant_id:{user.id}")

    
        

        try:
            await user.send(
                f"✅ Twoja aplikacja na serwerze **{guild.name}** na stanowisko Support została złożona! Zostaniesz powiadomiony o decyzji."
            )
        except discord.Forbidden:
            pass


class SupportApplyView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(
        label="Aplikuj na Support",
        style=discord.ButtonStyle.success,
        emoji="📝",
        custom_id="support_apply_button"
    )
    async def apply_support(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_modal(SupportApplicationModal())


# ===== SELECT MENU =====

class TicketSelect(discord.ui.Select):
    def __init__(self):
        options = [
            discord.SelectOption(
                label="Zgłoś błąd",
                description="Zgłoś błąd lub problem techniczny",
                emoji="🐛",
                value="zglos-blad"
            ),
            discord.SelectOption(
                label="Partnerstwo",
                description="Propozycja współpracy / partnerstwa",
                emoji="🤝",
                value="partnerstwo"
            ),
            discord.SelectOption(
                label="Propozycja",
                description="Zaproponuj propozycję lub nową funkcję",
                emoji="💡",
                value="propozycja"
            ),
            discord.SelectOption(
                label="Odbiór nagrody",
                description="Odbierz nagrodę z eventu lub konkursu",
                emoji="🎁",
                value="odbior-nagrody"
            ),
            discord.SelectOption(
                label="Inne",
                description="Wszystko inne",
                emoji="📩",
                value="inne"
            )
        ]

        super().__init__(
            placeholder="Wybierz kategorie ticketu...",
            min_values=1,
            max_values=1,
            options=options,
            custom_id="ticket_category_select"
        )

    async def callback(self, interaction: discord.Interaction):
        selected_value = self.values[0]

        mapping = {
            "zglos-blad": "🐛 Zgłoś błąd",
            "partnerstwo": "🤝 Partnerstwo",
            "propozycja": "💡 Propozycja",
            "odbior-nagrody": "🎁 Odbiór nagrody",
            "inne": "📩 Inne",
        }

        category_label = mapping[selected_value]
        modal = TicketModal(category_label=category_label, category_value=selected_value)
        await interaction.response.send_modal(modal)


class TicketPanelView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(TicketSelect())


# ===== EVENT READY =====

@bot.event
async def on_ready():
    bot.add_view(TicketPanelView())
    bot.add_view(TicketButtonsView())
    bot.add_view(SupportApplyView())
    bot.add_view(SupportApplicationButtons())
    print(f"Bot działa jako {bot.user}")

# ===== KOMENDA PANEL =====

@bot.command()
@commands.has_permissions(administrator=True)
async def panel(ctx):
    embed = discord.Embed(
        title="`   🎫 × System Ticketów         `",
        description="Potrzebujesz pomocy? Wybierz odpowiednią kategorię poniżej, aby otworzyć ticket.",
        color=discord.Color.dark_gray()
    )
    embed.set_footer(text="Counter-Strike • System Ticketów")

    # opcjonalny obrazek
    base_path = os.path.dirname(__file__)
    png_path = os.path.join(base_path, "ticket.png")
    jpg_path = os.path.join(base_path, "ticket.jpg")

    if os.path.exists(png_path):
        embed.set_image(url="attachment://ticket.png")
        file = discord.File(png_path, filename="ticket.png")
        await ctx.send(embed=embed, view=TicketPanelView(), file=file)
    elif os.path.exists(jpg_path):
        embed.set_image(url="attachment://ticket.jpg")
        file = discord.File(jpg_path, filename="ticket.jpg")
        await ctx.send(embed=embed, view=TicketPanelView(), file=file)
    else:
        await ctx.send(embed=embed, view=TicketPanelView())


@bot.command()
@commands.has_permissions(administrator=True)
async def panel2(ctx):
    embed = discord.Embed(
        title="` 📝 Counter-Strike × Rekrutacja na Support        `",
        description=(
            "**Chcesz dołączyć do naszego zespołu Support?**\n\n"
            "🟢 **Status: OTWARTA**\n\n"
            "| Kliknij przycisk poniżej, aby złożyć aplikację.\n"
            "| Twoja aplikacja zostanie rozpatrzona przez administrację.\n\n"
            "⚠️ Możesz mieć tylko jedną aktywną aplikację naraz."
        ),
        color=discord.Color.dark_gray()
    )

    embed.set_footer(text="Counter-Strike • Rekrutacja Support")

    await ctx.send(embed=embed, view=SupportApplyView())

@panel.error
async def panel_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("Tylko administrator może użyć tej komendy.")


# ===== DODATKOWE KOMENDY =====

@bot.command()
async def ping(ctx):
    await ctx.send("Pong! 🏓")


@bot.command()
async def hej(ctx):
    await ctx.send(f"Cześć {ctx.author.mention}!")


@bot.command()
async def add(ctx, member: discord.Member):
    if not ctx.channel.name.startswith("ticket-"):
        await ctx.send("Ta komenda działa tylko w tickecie.")
        return

    await ctx.channel.set_permissions(
        member,
        view_channel=True,
        send_messages=True,
        read_message_history=True,
        attach_files=True,
        embed_links=True
    )
    await ctx.send(f"Dodano {member.mention} do ticketu.")


@bot.command()
async def remove(ctx, member: discord.Member):
    if not ctx.channel.name.startswith("ticket-"):
        await ctx.send("Ta komenda działa tylko w tickecie.")
        return

    await ctx.channel.set_permissions(member, overwrite=None)
    await ctx.send(f"Usunięto {member.mention} z ticketu.")


@bot.command()
async def rename(ctx, *, new_name: str):
    if not ctx.channel.name.startswith("ticket-"):
        await ctx.send("Ta komenda działa tylko w tickecie.")
        return

    safe_name = sanitize_name(new_name)
    if not safe_name.startswith("ticket-"):
        safe_name = f"ticket-{safe_name}"

    await ctx.channel.edit(name=safe_name)
    await ctx.send(f"Zmieniono nazwę ticketu na `{safe_name}`.")


@bot.command()
@commands.has_permissions(manage_messages=True)
async def clear(ctx, amount: int):
    await ctx.channel.purge(limit=amount + 1)
    msg = await ctx.send(f"Usunięto {amount} wiadomości 🧹")
    await msg.delete(delay=3)


@clear.error
async def clear_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("Nie masz uprawnień do tej komendy.")
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Użycie: `!clear 5`")


bot.run(os.getenv("TOKEN"))

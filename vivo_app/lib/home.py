"""Helper utilities for home page parity work."""
from __future__ import annotations

from dataclasses import dataclass

from django.conf import settings


@dataclass(frozen=True)
class BookCover:
    """Lightweight representation of a faculty book cover."""

    author_id: str
    author_name: str
    title: str
    image_filename: str


BOOK_COVER_SAMPLE_DATA: list[BookCover] = [
    BookCover("jpallen", "James Allen", "Middle Egyptian Literature: Eight Literary Works of the Middle Kingdom", "Allen_MiddleEgyptianLiterature.jpg"),
    BookCover("pandreas", "Peter Andreas", "Rebel Mother: My Childhood Chasing the Revolution", "Andreas_RebelMother.jpg"),
    BookCover("rarenber", "Richard Arenberg", "Defending the Filibuster: The Soul of the Senate, Revised and Updated", "Arenberg_DefendingTheFilibuster.jpg"),
    BookCover("pbarmstr", "Paul Armstrong", "Norton Critical Edition of Joseph Conrad, Heart of Darkness, 5th ed", "Armstrong_HeartofDarkness.jpg"),
    BookCover("narpaly", "Nomy Arpaly", "In Praise of Desire", "arpaly.jpg"),
    BookCover("ebalk", "Ethan Balk", "Benefits and Harms of Routine Preoperative Testing", "Balk_BenefitsAndHarms.jpg"),
    BookCover("obartov", "Omer Bartov", "The Holocaust: Origins, Implementation, Aftermath", "Bartov_Holocaust.jpg"),
    BookCover("abenton", "Adia Benton", "HIV Exceptionalism: Development through Disease in Sierra Leone", "abenton.jpg"),
    BookCover("mblasing", "Mutlu Blasing", "Nazim Hikmet: The Life and Times of Turkey's World Poet", "blasing.jpg"),
    BookCover("mblyth", "Mark Blyth", "Austerity: The History of a Dangerous Idea", "blyth.jpg"),
    BookCover("ebrainer", "Elizabeth Brainerd", "Great Transformations in Vertebrate Evolution", "Brainerd_GreatTransformations.jpg"),
    BookCover("lbraun", "Lundy Braun", "Breathing Race into the Machine", "lbraun.jpg"),
]


def get_book_cover_pages(page_size: int) -> list[list[BookCover]]:
    """Return sample book cover data in pages mirroring Rails pagination."""
    pages: list[list[BookCover]] = []
    should_build_pages: bool = getattr(settings, "BOOK_COVER_STUB", True)
    if should_build_pages:
        current_page: list[BookCover] = []
        for cover in BOOK_COVER_SAMPLE_DATA:
            current_page.append(cover)
            if len(current_page) == page_size:
                pages.append(current_page)
                current_page = []
        if current_page:
            pages.append(current_page)
    return pages

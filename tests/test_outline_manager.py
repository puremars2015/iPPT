from agents.outline_manager import OutlineManager, OutlineParser


def test_outline_parser_handles_image_hint():
    items = OutlineParser.parse(["市場趨勢|bullet1,bullet2|image:trend.png"])
    assert len(items) == 1
    assert items[0].image_hint == "trend.png"
    assert items[0].bullets == ["bullet1", "bullet2"]


def test_outline_manager_splits_to_target_pages():
    items = OutlineParser.parse([
        "主題A|a1,a2,a3,a4",
        "主題B|b1,b2",
    ])
    manager = OutlineManager(target_pages=3)
    summary = manager.organize(items)
    assert len(summary.items) == 3
    titles = [item.title for item in summary.items]
    assert titles[0].startswith("主題A")
    assert any("Part 2" in title for title in titles)


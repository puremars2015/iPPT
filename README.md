
# 📑 AI PPT Agent – 最終規格書

## 1. 輸入介面

* **使用方式**：CLI 工具（不需要 GUI / API 第一版）
* **大綱輸入格式**：統一 CLI 文字格式

  ```
  "頁標題|bullet1,bullet2,bullet3"
  ```

  * 最小單位 = 一頁
  * `bullet` 清單 = 條列式重點
  * （未來擴充）可在最後加 `|image:xxx.jpg` 指定圖片

---

## 2. 模板解析 (Template Analyzer)

* 輸入：指定 `.pptx`
* 輸出：模板結構（JSON 格式，包含版型名稱、placeholder ID、字型、顏色、位置）
* 規則：

  * 保留 **字型大小 / 顏色 / 位置**
  * 版型分為 **常用 / 不常用**

    * 常用：`Title`、`Title+Content`、`Two-Content`
    * 其他 → 不常用

---

## 3. 大綱處理 (Outline Manager)

* **頁數控制**：

  * 使用者輸入「目標頁數」
  * 如果大綱項目數 < 頁數 → 拆分子項
  * 如果大綱項目數 > 頁數 → 合併相鄰項
  * 拆分/合併第一版用簡單規則，後續可用 AI 判斷
* **跨頁處理**：

  * 如果 bullet > 10 條 → 自動分成兩頁

---

## 4. 版型匹配 (Layout Matcher)

* 規則：

  * 優先使用 **常用 Layout**
  * 若無合適，fallback → `Title+Content`
  * 每頁一個大綱項目對應一個版型

---

## 5. 內容生成 (Content Generator)

* **文字**：

  * 用 AI 擴充 bullet → 轉換成「簡短補充句子」
  * 例如：

    * 輸入：`市場趨勢`
    * 輸出：`市場趨勢：AI 在製造業中逐漸普及`
* **圖片**：

  * 預設由 AI 自動生成，與 bullet 語意連結

    * 例如：bullet=`市場趨勢` → 自動生成「上升箭頭圖」
  * 不需要自動塞進圖片 placeholder（先輸出圖片檔路徑，使用者自行插入或後續版本再自動化）

---

## 6. 投影片生成 (Slide Generator)

* 保留 **模板母片設計**：字型、顏色、頁腳、Logo
* 若 placeholder 缺失 → 跳過，不報錯
* 每頁填入：

  * 標題 → title placeholder
  * 條列 → content placeholder
  * 圖片（未來版本再考慮自動塞入）

---

## 7. 輸出規範

* 檔名：固定 `output.pptx`
* 無頁數/效能限制
* 單次生成 10 頁 or 100 頁都允許

---

## 8. 錯誤處理

* 模板缺少 placeholder → 跳過
* 大綱項目數與頁數不符 → 系統自動拆分/合併
* 若圖片生成失敗 → 保留文字，不阻塞流程

---




---

# 📌 AI PPT Agent – 工作流程範例

## 🎯 使用者輸入

```bash
python ppt_agent.py \
  --template templates/company_template.pptx \
  --title "AI 在製造業的應用" \
  --pages 5 \
  --outline "封面|公司名稱,講者" \
           "市場趨勢|數位轉型,自動化需求,人力成本上升" \
           "導入步驟|需求盤點,資料整理,PoC,全面導入" \
           "效益|提升產能,降低成本,優化決策" \
           "結論|下一步行動,團隊目標"
```

---

## 🛠️ 系統處理步驟

### 1. Template Analyzer (模板解析)

* 讀取 `company_template.pptx`
* 輸出結構（示意 JSON）：

```json
[
  {"layout_name": "Title Slide", "kind": "title", "placeholders": {"title":0,"subtitle":1}},
  {"layout_name": "Title and Content", "kind": "text", "placeholders": {"title":0,"content":1}},
  {"layout_name": "Two Content", "kind": "text", "placeholders": {"title":0,"content":1}},
  {"layout_name": "Comparison", "kind": "text", "placeholders": {"title":0,"content":1}},
  ...
]
```

* 常用 = Title Slide, Title and Content, Two Content

---

### 2. Outline Manager (大綱處理)

* 使用者輸入 **5 頁** → 大綱剛好 5 項，不需要拆分/合併
* 每個大綱項目就是一頁

---

### 3. Layout Matcher (版型匹配)

* 對應結果：

  * `封面` → Title Slide
  * `市場趨勢` → Title and Content
  * `導入步驟` → Title and Content
  * `效益` → Title and Content
  * `結論` → Title and Content

---

### 4. Content Generator (AI 擴充內容)

* 對應大綱 → AI 補充簡短句子：

  * `數位轉型` → `數位轉型：企業正加速導入 AI 技術`
  * `自動化需求` → `自動化需求：提升效率以應對全球競爭`
  * `人力成本上升` → `人力成本上升：智能化可降低長期支出`

* 圖片生成：

  * `市場趨勢` → 自動生成「上升箭頭」圖片 → 輸出到 `output/images/trend.png`

---

### 5. Slide Generator (投影片產生)

* 保留模板的 **字型 / 顏色 / Logo**
* 填充內容：

  * 封面 → Title (AI 在製造業的應用)，Subtitle (公司名稱, 講者)
  * 內容頁 → Title = 大綱標題，Content = 條列式 bullets
  * 若圖片生成成功 → 輸出檔案，暫不自動插入

---

## 📤 輸出

* 檔名：`output.pptx`
* 檔案結構：

```
output/
 ├─ output.pptx
 └─ images/
     └─ trend.png
```

---

## 🖼️ 最終 PPT 頁面示意

1. **封面**（Title Slide）

   ```
   AI 在製造業的應用
   公司名稱 | 講者
   ```

   （套用公司模板樣式）

2. **市場趨勢**（Title + Content）

   * 數位轉型：企業正加速導入 AI 技術
   * 自動化需求：提升效率以應對全球競爭
   * 人力成本上升：智能化可降低長期支出
     [圖片檔：trend.png]

3. **導入步驟**

   * 需求盤點：評估企業痛點與機會
   * 資料整理：確保數據可用性
   * PoC：小規模試點驗證
   * 全面導入：擴散到產線

4. **效益**

   * 提升產能：自動化流程提高效率
   * 降低成本：優化人力與資源配置
   * 優化決策：AI 輔助分析

5. **結論**

   * 下一步行動：建立 AI 專案小組
   * 團隊目標：三年內達成 30% 自動化率

---

✅ 這個例子清楚展示了：

* 使用者怎麼輸入
* 系統怎麼判斷模板 + 分配大綱
* AI 怎麼擴充 bullet
* 最後 PPT 長什麼樣

---

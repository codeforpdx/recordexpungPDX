import React, { useState, useRef, useEffect } from "react";
import OregonMap from "./OregonMap";
import { oregonCounties, County, Post } from "../../data/countyPosts";
import {
  countyFilingData,
  CountyFilingInfo,
} from "../../data/countyFilingData";
import setupPage from "../../service/setupPage";

function CountySidebar({
  selectedCounty,
  hoveredCounty,
  hoverSource,
  onSelectCounty,
  onHoverCounty,
  maxHeight,
}: {
  selectedCounty: string | null;
  hoveredCounty: string | null;
  hoverSource: "map" | "list" | null;
  onSelectCounty: (countyName: string) => void;
  onHoverCounty: (countyName: string | null, source: "map" | "list") => void;
  maxHeight: number;
}) {
  const containerRef = useRef<HTMLDivElement>(null);
  const itemRefs = useRef<Map<string, HTMLLIElement>>(new Map());

  useEffect(() => {
    if (hoveredCounty && hoverSource === "map" && containerRef.current) {
      const item = itemRefs.current.get(hoveredCounty);
      if (item) {
        const container = containerRef.current;
        const containerRect = container.getBoundingClientRect();
        const itemRect = item.getBoundingClientRect();
        const itemRelativeTop = itemRect.top - containerRect.top + container.scrollTop;
        const targetScroll = itemRelativeTop - containerRect.height / 2 + itemRect.height / 2;
        container.scrollTo({ top: targetScroll, behavior: "smooth" });
      }
    }
  }, [hoveredCounty, hoverSource]);

  const handleCountyClick = (countyName: string) => {
    if (selectedCounty === countyName) {
      onSelectCounty("");
    } else {
      onSelectCounty(countyName);
    }
  };

  return (
    <div ref={containerRef} className="bl b--light-gray pl3 overflow-y-auto" style={{ width: "200px", maxHeight: maxHeight || 400 }}>
      <h2 className="f5 fw7 mb3">Oregon Counties</h2>
      <ul className="list pl0 ma0">
        {oregonCounties.map((county) => (
          <li
            key={county.name}
            ref={(el) => {
              if (el) itemRefs.current.set(county.name, el);
            }}
            className={`pv1 ph2 pointer br2 ${
              selectedCounty === county.name
                ? "bg-blue white"
                : hoveredCounty === county.name
                ? "bg-lightest-blue"
                : "hover-bg-light-gray"
            }`}
            onClick={() => handleCountyClick(county.name)}
            onMouseEnter={() => onHoverCounty(county.name, "list")}
            onMouseLeave={() => onHoverCounty(null, "list")}
          >
            {county.name}{" "}
            <span className={selectedCounty === county.name ? "white-70" : "gray"}>{" "}({county.posts.length})</span>
          </li>
        ))}
      </ul>
    </div>
  );
}

function FilingNotesSection({ county }: { county: string }) {
  const info: CountyFilingInfo | undefined = countyFilingData[county];
  const waitMonths = info?.waitMonths ?? 4;
  const notes = info?.notes ?? [];

  const [showTipsForm, setShowTipsForm] = useState(false);
  const [tips, setTips] = useState("");
  const [nameOrg, setNameOrg] = useState("");
  const [status, setStatus] = useState<"idle" | "submitting" | "success" | "error">("idle");

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!tips.trim()) return;

    setStatus("submitting");
    try {
      const response = await fetch("https://formspree.io/f/xeeovpoj", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          type: "Offer filing tips",
          county,
          message: tips,
          name: nameOrg || "(anonymous)",
          _subject: `Filing Tips: ${county} County`,
        }),
      });

      if (response.ok) {
        setStatus("success");
      } else {
        setStatus("error");
      }
    } catch {
      setStatus("error");
    }
  };

  return (
    <div className="mb4">
      <h3 className="f5 fw7 mb2">Filing Notes</h3>
      <ul className="list pl3 ma0">
        <li className="mb1">Estimated response time: {waitMonths} months</li>
        {notes.map((note, idx) => (
          <li key={idx} className="mb1">
            {note}
          </li>
        ))}
      </ul>

      <div className="mt3">
        {status === "success" ? (
          <p className="green fw6">Thank you! Your tips will be reviewed and added soon.</p>
        ) : !showTipsForm ? (
          <p className="f6">
            If you are a provider in this county,{" "}
            <button
              type="button"
              className="bg-transparent bn blue pointer underline pa0 f6"
              onClick={() => setShowTipsForm(true)}
            >
              Offer filing tips
            </button>
          </p>
        ) : (
          <form onSubmit={handleSubmit} className="mt2">
            <input type="text" name="_gotcha" style={{ display: "none" }} tabIndex={-1} autoComplete="off" />
            {status === "error" && (
              <p className="dark-red mb2">Something went wrong. Please try again.</p>
            )}
            <textarea
              className="w-100 pa2 br2 ba b--light-gray mb2"
              placeholder="Share filing tips for this county..."
              rows={3}
              value={tips}
              onChange={(e) => setTips(e.target.value)}
              required
            />
            <div className="mb2">
              <label htmlFor="tips-name-org" className="db f6 mb1">
                Your name & organization:
              </label>
              <input
                id="tips-name-org"
                type="text"
                className="w-100 pa2 br2 ba b--light-gray"
                value={nameOrg}
                onChange={(e) => setNameOrg(e.target.value)}
                required
              />
            </div>
            <button
              type="submit"
              className="bg-blue white fw6 br2 pv2 ph3 pointer bn"
              disabled={status === "submitting"}
            >
              {status === "submitting" ? "Submitting..." : "Submit"}
            </button>
            <button
              type="button"
              className="bg-lightest-blue dark-blue fw6 br2 pv2 ph3 pointer bn ml2"
              onClick={() => setShowTipsForm(false)}
            >
              Cancel
            </button>
          </form>
        )}
      </div>
    </div>
  );
}

function CommentsSection({ posts, county }: { posts: Post[]; county: string }) {
  const [title, setTitle] = useState("");
  const [message, setMessage] = useState("");
  const [name, setName] = useState("");
  const [status, setStatus] = useState<"idle" | "submitting" | "success" | "error">("idle");
  const [showAllComments, setShowAllComments] = useState(false);

  const visiblePosts = showAllComments ? posts : posts.slice(0, 3);
  const hasMoreComments = posts.length > 3;

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!title.trim() || !message.trim()) return;

    setStatus("submitting");
    try {
      const response = await fetch("https://formspree.io/f/xeeovpoj", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          type: "Share your experience",
          county,
          title,
          message,
          name: name || "(anonymous)",
          _subject: `Community Post: ${county} County`,
        }),
      });

      if (response.ok) {
        setStatus("success");
      } else {
        setStatus("error");
      }
    } catch {
      setStatus("error");
    }
  };

  return (
    <div className="mb4">
      <h3 className="f5 fw7 mb2">Comments</h3>
      {posts.length === 0 ? (
        <p className="gray i">No comments yet for this county.</p>
      ) : (
        <div>
          {visiblePosts.map((post) => (
            <div key={post.id} className="bg-white pa3 mb2 br2 shadow-1">
              <h4 className="f6 fw7 mv0 mb1">{post.title}</h4>
              <p className="f6 mv0 gray">{post.preview}</p>
              {post.name && <p className="f6 mv0 mt2 i">-{post.name}</p>}
            </div>
          ))}
          {hasMoreComments && !showAllComments && (
            <button
              type="button"
              className="bg-light-gray dark-gray fw6 br2 pv2 ph3 pointer bn mt2"
              onClick={() => setShowAllComments(true)}
            >
              Show {posts.length - 3} more comment{posts.length - 3 > 1 ? "s" : ""}
            </button>
          )}
        </div>
      )}

      {status === "success" ? (
        <div className="mt3 pt3 bt b--light-gray">
          <p className="green fw6">Thank you! Your post will be reviewed and shared soon!</p>
        </div>
      ) : (
        <form onSubmit={handleSubmit} className="mt3 pt3 bt b--light-gray">
          <input type="text" name="_gotcha" style={{ display: "none" }} tabIndex={-1} autoComplete="off" />
          <h4 className="f6 fw7 mv0 mb3">Share your experience</h4>
          {status === "error" && (
            <p className="dark-red mb2">Something went wrong. Please try again.</p>
          )}
          <div className="mb2">
            <label htmlFor="post-title" className="db f6 mb1">
              Title:
            </label>
            <input
              id="post-title"
              type="text"
              className="w-100 pa2 br2 ba b--light-gray"
              placeholder="Give your post a title..."
              value={title}
              onChange={(e) => setTitle(e.target.value)}
              required
            />
          </div>
          <textarea
            className="w-100 pa2 br2 ba b--light-gray mb2"
            placeholder="Share your experience with record expungement in this county..."
            rows={4}
            value={message}
            onChange={(e) => setMessage(e.target.value)}
            required
          />
          <div className="mb2">
            <label htmlFor="post-name" className="db f6 mb1">
              Your name (optional):
            </label>
            <input
              id="post-name"
              type="text"
              className="w-100 pa2 br2 ba b--light-gray"
              placeholder=""
              value={name}
              onChange={(e) => setName(e.target.value)}
            />
          </div>
          <button
            type="submit"
            className="bg-blue white fw6 br2 pv2 ph3 pointer bn"
            disabled={status === "submitting"}
          >
            {status === "submitting" ? "Posting..." : "Post"}
          </button>
        </form>
      )}
    </div>
  );
}

function CountyContent({
  county,
  onClose,
}: {
  county: County;
  onClose: () => void;
}) {
  return (
    <div
      className="bg-near-white pa4"
      style={{ flex: "1 1 400px" }}
    >
      <div className="flex justify-between items-center mb3">
        <h2
          className="f4 fw7 mv0 pointer hover-blue"
          onClick={onClose}
        >
          {county.name} County
        </h2>
        <button
          className="bg-transparent bn f4 pointer gray hover-blue"
          onClick={onClose}
          aria-label="Close county panel"
        >
          &gt;&gt;
        </button>
      </div>

      <FilingNotesSection county={county.name} />
      <CommentsSection posts={county.posts} county={county.name} />
    </div>
  );
}

export default function Community() {
  setupPage("Community Message Board");

  const [selectedCounty, setSelectedCounty] = useState<string | null>(null);
  const [hoveredCounty, setHoveredCounty] = useState<string | null>(null);
  const [hoverSource, setHoverSource] = useState<"map" | "list" | null>(null);
  const [mapHeight, setMapHeight] = useState<number>(400);
  const mapContainerRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const updateHeight = () => {
      if (mapContainerRef.current && !selectedCounty) {
        setMapHeight(mapContainerRef.current.offsetHeight);
      }
    };
    updateHeight();
    window.addEventListener("resize", updateHeight);
    return () => window.removeEventListener("resize", updateHeight);
  }, [selectedCounty]);

  const handleSelectCounty = (countyName: string) => {
    setSelectedCounty(countyName === "" ? null : countyName);
  };

  const handleHoverCounty = (countyName: string | null, source: "map" | "list") => {
    setHoveredCounty(countyName);
    setHoverSource(countyName ? source : null);
  };

  const selectedCountyData = oregonCounties.find(
    (county) => county.name === selectedCounty
  );

  return (
    <main className="mw8 center f6 f5-l ph3 pt4 pb6">
      <h1 className="f3 f2-l fw9 mb4">Community Message Board</h1>
      <p className="lh-copy mb4 mw7">
        Select a county on the map or from the list to see local resources,
        filing notes, and community experiences with record expungement.
      </p>

      <div className="flex items-start">
        <div
          ref={mapContainerRef}
          className={`transition-all ${
            selectedCounty ? "w-30" : "w-60"
          }`}
          style={{ minWidth: selectedCounty ? "200px" : "400px" }}
        >
          <OregonMap
            selectedCounty={selectedCounty}
            hoveredCounty={hoveredCounty}
            onSelectCounty={handleSelectCounty}
            onHoverCounty={handleHoverCounty}
          />
        </div>

        {selectedCountyData && (
          <CountyContent
            county={selectedCountyData}
            onClose={() => setSelectedCounty(null)}
          />
        )}

        <CountySidebar
          selectedCounty={selectedCounty}
          hoveredCounty={hoveredCounty}
          hoverSource={hoverSource}
          onSelectCounty={handleSelectCounty}
          onHoverCounty={handleHoverCounty}
          maxHeight={mapHeight}
        />
      </div>
    </main>
  );
}

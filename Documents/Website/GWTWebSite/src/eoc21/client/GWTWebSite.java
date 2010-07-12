package eoc21.client;

import java.util.ArrayList;

import com.google.gwt.core.client.EntryPoint;
import com.google.gwt.user.client.ui.RootPanel;
import com.smartgwt.client.widgets.layout.HLayout;
import com.smartgwt.client.widgets.layout.SectionStack;

/**
 * Entry point classes define <code>onModuleLoad()</code>.
 */
public class GWTWebSite implements EntryPoint {
	/**
	 * This is the entry point method.
	 */
	public void onModuleLoad() {
		
		RecentUpdatesPanel recentUpdatesPanel = new RecentUpdatesPanel();
		SectionStack newsStack = recentUpdatesPanel.setUpPanel();
	//	SectionStack rs = recentUpdatesPanel.setUpPanel();
		ArrayList<SectionStack> sections = new ArrayList<SectionStack>();
		sections.add(0, newsStack);
	//	sections.add(1,rs);
		LayoutManager4Website.getInstance(sections);
		HLayout hlay = LayoutManager4Website.getInstance(sections).getHLayout();
		RootPanel.get().add(hlay);

	}
}
